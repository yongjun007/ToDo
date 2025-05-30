# --------------------------------------------------------
# 파일명 : task.py
# 위치 : api/models/task.py
# 이 파일은 데이터베이스의 'task'와 'dones' 테이블에
# 대응되는 SQLAlchemy 모델 클래스(Task, Done)를 정의한다.
# --------------------------------------------------------

# --------------------------------------------------------
# SQLAlchemy에서 테이블을 정의할 때 필요한 기능들을 불러온다
# --------------------------------------------------------
from sqlalchemy import Column, Integer, String, ForeignKey, Date

# * Column: 테이블의 각 열(컬럼)을 정의할 떄 사용
# * Integer: 정수형 데이터 타입 (예: ID)
# * string: 문자열 데이터 타입 (예: 제목)
# * ForeignKet: 다른 테이블의 값을 참조할 떄 사용 (외래키 설정)
# * Date: 날짜 데이터 타입 (예: 마감일)

from sqlalchemy.orm import relationship

# * 테이블 간의 관계(1:1, 1:N 등)를 정의할 떄 사용하는 도구
# * 예: Task와 Done이 서로 연결되도록 설정할 수 있음

from api.db import Base  # SQLAlchemy에서 사용하는 모델의 기반 클래스


# -------------------------------------------------------------
# [1] Task 모델 > tasks 테이블과 매핑됨
# ------------------------------------------------------------
class Task(Base):
    __tablename__ = "tasks"  # 이 클래스는 'tasks' 테이블과 연결됨

    id = Column(Integer, primary_key=True)
    # > DB 컬럼: tasks.id
    # * SQLAlchemy: Integer + primary_key=true
    # * PostgreSQL: SERIAL PRIMARY KEY (자동 증가 정수, 기본키)

    title = Column(String(1024))
    due_date = Column(Date)
    # > DB 컬럼 : task.title
    # * SQLAlchemy: String(1024)
    # * PostgreSQL: VARCHAR(1024)

    done = relationship("Done", back_populates="task", cascade="all, delete")
    # * Task <> Done: 1:1 관계
    # * done :연결된 Done 객체 (완료여부)를 참조함
    # * cascade="all, delete" > Task 삭제 시 연결된 Done도 함께 삭제됨

    # ------------------------------------------------
    # [2] Done 모델 > dones 테이블과 매핑됨
    # ------------------------------------------------


class Done(Base):
    __tablename__ = "dones"  # 이 클래스는 'dones' 테이블과 연결됨

    id = Column(Integer, ForeignKey("tasks.id"), primary_key=True)
    # > DB 컬럼 : dones.id (외래키: tasks.id)
    # * SQLAlchemy: Integer + ForeignKey + primary_key=True
    # * PostgreSQL: INTEGER + FOREIGN KEY + PRIMARY KEY
    # * 1:1 관계 유지: dones.id = tasks.id 인 상태
    # * 완료된 작업만 이 테이블에 기록됨

    task = relationship("Task", back_populates="done")
    # * 연결된 Task 객체를 참조할 수 있음
    # * task: Done > Task 방향 참조
