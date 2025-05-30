# ----------------------------------------------------------------------
# 파일명: test_setup.py (예시)
# 목적: FastAPI 앱을 테스트할 수 있도록 설정하는 코드입니다.
# - 실제 DB를 사용하지 않고, 메모리에서만 동작하는 임시 DB를 사용합니다.
# - FastAPI 앱이 이 테스트용 DB를 사용하도록 바꿔줍니다.
# ----------------------------------------------------------------------

# 테스트 도구: pytest는 파이썬 테스트 프레임워크
import pytest

# 비동기 테스트 지원: pytest에서 async 함수도 테스트 가능하게 해줍니다
import pytest_asyncio

# httpx: 코드로 HTTP 요청을 보낼 수 있는 클라이언트 (FastAPI와 잘 호환됨)
from httpx import AsyncClient, ASGITransport

# SQLAlchemy 비동기 전용 모듈
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker

# 프로젝트 내부 코드 불러오기 (DB 세션 함수, DB 모델, FastAPI 앱)
from api.db import get_db, Base
from api.main import app

# 타입 힌트를 위한 모듈
from typing import AsyncGenerator

# HTTP 상태 코드를 직관적인 이름으로 사용하기 위해 불러옴
# 예: status.HTTP_200_OK, status.HTTP_404_NOT_FOUND 등
import starlette.status as status

# -----------------------------------------------------------------------
# ASYNC_DB_URL: 테스트에 사용할 임시 SQLite 데이터베이스 주소
# - ":memory:"는 실제 파일을 만들지 않고, 메모리에만 저장함
# - 테스트가 끝나면 DB 내용은 모두 사라짐
# ----------------------------------------------------------------------
ASYNC_DB_URL = "sqlite+aiosqlite:///:memory:"


# -------------------------------------------------------------------------
# async_client: 테스트에서 사용할 비동기 HTTP 클라이언트를 만드는 함수
# - 이 함수는 fixture로 등록되어 여러 테스트에서 공통으로 사용 가능
# - yield를 사용하므로 AsyncGenerator로 타입 지정해야 함
# -------------------------------------------------------------------------
@pytest_asyncio.fixture
async def async_client() -> AsyncGenerator[AsyncClient, None]:
    # --------------------------------------------------------------------
    # 1. 테스트용 비동기 DB 엔진과 세션 생성기 설정
    # - 실제 서브스용 DB와는 완전히 분리됨
    # --------------------------------------------------------------------
    async_engine = create_async_engine(ASYNC_DB_URL, echo=True)
    async_session = sessionmaker(
        autocommit=False,  # 명시적으로 commit 해야 저장됨
        autoflush=False,  # flush 타이밍도 직접 제어
        bind=async_engine,  # 위에서 만든 비동기 DB 엔진 사용
        class_=AsyncSession,  # 세션은 비동기 방식으로 사용
    )

    # ------------------------------------------------------------------
    # 2. 테스트용 DB 초기화 (테이블 전체 삭제 후 재생성)
    # ------------------------------------------------------------------
    async with async_engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)  # 기존 테이블 제거
        await conn.run_sync(Base.metadata.create_all)  # 필요한 테이블 생성

    # -------------------------------------------------------
    # 3. get_db() 함수를 테스트용 DB와 연결되도록 override
    # - 실제 앱에서 사용하는 DB 대신 테스트용 DB로 작동하게 만듦
    # -------------------------------------------------------
    async def get_test_db():
        async with async_session() as session:
            yield session
            # yield는 session을 외부로 잠깐 넘기고, 끝나면 정리 작업 실행

    app.dependency_overrides[get_db] = get_test_db

    # ------------------------------------------------------------
    # 4. 테스트용 HTTP 클라이언트 생성
    # - FastAPI 서버를 실제로 띄우지 않아도 요청을 보낼 수 있음
    # - base_url은 내부적으로만 사용되는 테스트 주소
    # ------------------------------------------------------------
    transport = ASGITransport(app=app, raise_app_exceptions=True)
    async with AsyncClient(transport=transport, base_url="http://test") as client:
        yield client
        # 테스트 함수에서 이 client를 사용하면, 실제 서버 없어도 앱에 요청 가능


# -------------------------------------------------------------------
# [테스트 함수] 할 일 생성 및 목록 조회 테스트
# - POST /tasks로 할 일을 하나 추가하고
# - GET /tasks로 전체 목록을 조회해 결과를 검증합니다
# -------------------------------------------------------------------
@pytest.mark.asyncio
async def test_create_and_read(async_client):
    # ---------------------------------------------------------------
    # 1. 새로운 할 일을 추가 (POST 요청)
    # - title이 "테스트 작업"인 할 일을 서버에 추가 요청
    # ---------------------------------------------------------------
    response = await async_client.post("/tasks", json={"title": "테스트 작업"})
    assert response.status_code == status.HTTP_200_OK  # 응답이 200 OK 인지 확인

    response_obj = response.json()
    assert (
        response_obj["title"] == "테스트 작업"
    )  # 응답 JSON에 title이 잘 들어갔는지 확인

    # ----------------------------------------------
    # 2. 전체 할 일 목록 조회 (GET 요청)
    # - 방금 추가한 할 일이 목록에 포함되어 있는지 확인
    # ----------------------------------------------
    response = await async_client.get("/tasks")
    assert response.status_code == status.HTTP_200_OK  # 200 OK 확인

    response_obj = response.json()
    assert len(response_obj) == 1  # 할 일 개수가 1개인지 확인
    assert response_obj[0]["title"] == "테스트 작업"  # 그 할 일의 제목이 정확한지 확인
    assert response_obj[0]["done"] is False  # 완료 여부가 False인지 확인 (기본값)


@pytest.mark.asyncio
async def test_done_flag(async_client):
    # ---------------------------------------------------
    # [1] 새로운 할 일을 추가 (POST 요청)
    # - title이 "테스트 작업2"인 할 일을 서버에 추가 요청
    # ---------------------------------------------------
    response = await async_client.post("/tasks", json={"title": "테스트 작업2"})
    assert response.status_code == status.HTTP_200_OK  # 요청이 성공 했는지 확인
    response_obj = response.json()  # 응답 결과를 JSON 형식으로 변환
    assert response_obj["title"] == "테스트 작업2"  # title 값이 올바른지 확인

    # ----------------------------------------------------------------------------
    # [2] 할 일을 완료 처리 (PUT 요청)
    # - 이 테스트에서는 PUT /tasks 라는 주소에 요청을 보냄
    # - 실제 구현에서는 가장 마지막에 추가된 작업을 완료 처리하는 방식일 수 있음
    # - 즉, 우리가 방금 추가한 "테스트 작업2"가 완료 처리됨
    # ----------------------------------------------------------------------------
    response = await async_client.put("/tasks/1/done")
    assert (
        response.status_code == status.HTTP_200_OK
    )  # 완료 처리 요청이 성공했는지 확인

    # ---------------------------------------------------------------
    # [3] 이미 완료된 할 일을 다시 완료 처리 시도 (PUT 요청)
    # - /tasks/1/done 주소로 요청을 보내 id=1인 작업을 완료 처리하려고 시도함
    # - 하지만 이미 완료도니 작업이므로 서버가 400 Bad Request를 반환해야 함
    # --------------------------------------------------------------
    response = await async_client.put("/tasks/1/done")
    assert (
        response.status_code == status.HTTP_400_BAD_REQUEST
    )  # 중복 완료 요청 > 잘못된 요청 처리 확인

    # -------------------------------------------------------------
    # [4] 완료 처리된 작업을 완료 해제 (DELETE 요청)
    # - /tasks/1/done 주소로 요청을 보내면 완료 상태가 해제됨 (False로 변경됨)
    # ------------------------------------------------------------
    response = await async_client.delete("/tasks/1/done")
    assert (
        response.status_code == status.HTTP_200_OK
    )  # 정상적으로 완료 해제되었는지 확인
    # ----------------------------------------------------
    # [5] 이미 완료 해제된 작업을 다시 해제하려고 시도
    # - 더 이상 완료상태가 아니므로 서버는 해당 작업이 존재하지 않는다고 판단
    # - 따라서 404  Not Found 응답을 보내는 것이 올바름
    # -----------------------------------------------------
    response = await async_client.delete("/tasks/1/done")
    assert (
        response.status_code == status.HTTP_404_NOT_FOUND
    )  # 존재하지 않는 상태를 다시 요청 > 실패 응답 확인


# ---------------------------------------------------
# 테스트 목적: 마감일 (due_date)의 유효성 검사
# ---------------------------------------------------
# 이 테스트 함수는 사용자가 할 일을 등록할 떄 입력하느 'due_date' 값이
# 유효하지 않은 날짜이거나 올바른 형식이 아닐 경우 서버가 어떻게 반응하는지 확인합니다.
#
# [검사 항목]
# (1) 올바른 날짜 입력 시 정상 처리 (200 OK)
# (2) 존재하지 않는 날짜 (예: 12월 32일) > 오류 반환 (422)
# (3) 잘모된 구분자 사용 (예: 2024/12/01) > 오류 반환 (422)
# (4) 구분자 없이 숫자만 나열 (예: 20241201) > 오류 반환 (422)
#
# 이 검사를 통 FastAPI + Pydantic이 날짜 형식을 어떻게 검사하는지 이해할 수 있습니다.
# -----------------------------------------------------------
@pytest.mark.asyncio
@pytest.mark.parametrize(
    "input_param, expectation",  # 매개변수 이름 정의
    [
        ("2024-12-01", status.HTTP_200_OK),
        ("2024-12-32", status.HTTP_422_UNPROCESSABLE_ENTITY),
        ("2024/12/01", status.HTTP_422_UNPROCESSABLE_ENTITY),
        ("20241201", status.HTTP_422_UNPROCESSABLE_ENTITY),
    ],
)
async def test_due_date(async_client, input_param, expectation):
    # ------------------------------------------------------------
    # 1. 비동기 POST 요청 전송
    # - /tasks 경로에 JSON 데이터 (title과 due_date)를 전송합니다.
    # - input_param은 각 테스트 케이스에서 주어진 날짜 형식 문자열입니다.
    # ------------------------------------------------------------
    response = await async_client.post(
        "/tasks",
        json={
            "title": "테스트 작업",
            "due_date": input_param,  # 현재 테스트할 날짜 문자열
        },
    )
    # ---------------------------------------------------------------
    assert response.status_code == expectation
