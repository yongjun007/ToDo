# -----------------------------------------------------------
# 파일명: done.py
# 위치: api/schemas/done.py
# 이 파일은 "응답 데이터 형식"을 정의한 곳입니다.
# FastAPI는 사용자의 요청에 대한 응답을 JSON 형식으로 보냅니다.
# 여기서는 완료된 할 일(Done)에 대한 응답 구조를 정의합니다.
# -----------------------------------------------------------

from pydantic import BaseModel, Field, ConfigDict

# - BaseModel: 모든 데이터 구조의 기본이 되는 클래스
# - Field: 각 항목에 기본값, 예시, 설명 등을 붙일 수 있게 해준다
# - ConfigDict: Pydantic v2 부터 모델 설정 (예: from_attributes)을 지정할 떄 사용


# -----------------------------------------------------
# DoneResponse 클래스
# - 할 일이 완료되었을 떄 응답에 사용되는 형식입니다.
# - 예: {"id: 3"} 이면, 3번 할 일이 완료되었음을 의미합니다.
# -----------------------------------------------------
class DoneResponse(BaseModel):
    id: int  # 완료된 할 일의 번호

    # Config 클래스 설정
    # - from_attributes = True 를 설정하면,
    #   SQLAlchemy 모델 객체를 그대로 사용할 수 있습니다.
    # - pydantic 2버전에서는 기존 orm_mode = True 대신
    #   from_attributes = True 를 사용해야 경고 없이 동작합니다.
    model_config = ConfigDict(from_attributes=True)
