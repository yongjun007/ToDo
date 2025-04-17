# ---------------------------------------------------------------------
# 파일명: migrate_db.py
# 위치 : api/migrate_db.py
# 이 파일은 데이터베이스 테이블을 초기화(삭제 후 재성성)하는 스크립트이다.
# - 수업이나 개발 과정에서 테이블 구조를 바꾼 뒤 다시 적용할 때 사용한다.
# - 기존 테이블을 모두 삭제(drop)한 후 새로 생성(create)한다.
# ---------------------------------------------------------------------

from sqlalchemy import create_engine  # DB 연결을 위한 SQLAlchemy 도구
from api.models.task import Base  # 테이블 구조가 정의된 모델의 기반 클래스

# ---------------------------------------------------------------------
# PostgreSQL 연결 주소 설정 (동기용 드라이버 사용)
# 형식: postgresql+psycopg2://[사용자]:[비밀번호]@[호스트]/[DB이름]
# - 비동기 드라이버(asyncpg)가 아닌 동기 드라이버(psycopg2)를 사용해야 오류가 발생하지 않음
# ---------------------------------------------------------------------
DB_URL = "postgresql+psycopg2://todo_user:1234@localhost/todo_db"

# ---------------------------------------------------------------------
# SQLAlchemy의 동기 엔진 생성
# * create_engine()은 동기용이므로 psycopg2와 함께 사용해야 함
# * echo=True > 실행되는 SQL문이 터미널에 출력됨 (디버깅에 유용)
# ---------------------------------------------------------------------
engine = create_engine(DB_URL, echo=True)

# ---------------------------------------------------------------------
# 데이터베이스 초기화 함수
# - 기존 테이블을 모두 삭제(drop)
# - 모델에 정의된 테이블 구조로 다시 생성(create)


def reset_database():
    Base.metadata.drop_all(bind=engine)  # 모든 테이블 삭제
    Base.metadata.create_all(bind=engine)  # 테이블 새로 생성


# ---------------------------------------------------------------------
# 이 파일을 직접 실행하면 reset_database 함수가 실행된다.
# ---------------------------------------------------------------------
if __name__ == "__main__":
    reset_database()
