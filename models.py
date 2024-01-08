from fastapi_users_db_sqlalchemy import SQLAlchemyBaseUserTable
from sqlalchemy import Column, Integer, String, TIMESTAMP, ForeignKey, Boolean
from datetime import datetime
from sqlalchemy.orm import DeclarativeBase, DeclarativeMeta, declarative_base, Mapped, mapped_column
from enums.enums import Status

Base: DeclarativeMeta = declarative_base()


class Base(DeclarativeBase):
    pass


class Task(Base):
    __tablename__ = "tasks"

    number = Column(Integer, primary_key=True, autoincrement=True)
    type = Column(String, nullable=False)
    priority = Column(String, nullable=True)
    status = Column(String, nullable=False, default=Status.To_do)
    header = Column(String, nullable=False)
    description = Column(String, nullable=True)
    executor = Column(Integer, ForeignKey('users.id', ondelete="NO ACTION"), nullable=True)
    creator = Column(Integer, ForeignKey('users.id', ondelete="NO ACTION"), nullable=False)
    time_of_creation = Column(TIMESTAMP, nullable=False, default=datetime.utcnow)
    time_of_modification = Column(TIMESTAMP, nullable=False, default=datetime.utcnow)


class Subtasks(Base):
    __tablename__ = "Subtasks"

    id = Column(Integer, primary_key=True, autoincrement=True)
    main_task = Column(Integer, ForeignKey('tasks.number', ondelete="CASCADE"), nullable=False)
    sub_task = Column(Integer, ForeignKey('tasks.number', ondelete="CASCADE"), nullable=False)


class User(SQLAlchemyBaseUserTable[int], Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(
        Integer, autoincrement=True, nullable=False, primary_key=True
    )
    email: Mapped[str] = mapped_column(
        String(length=320), unique=True, index=True, nullable=False
    )
    hashed_password: Mapped[str] = mapped_column(
        String(length=1024), nullable=False
    )
    role: Mapped[str] = mapped_column(
        String(length=20), nullable=False
    )
    is_active: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)
    is_superuser: Mapped[bool] = mapped_column(
        Boolean, default=False, nullable=False
    )
    is_verified: Mapped[bool] = mapped_column(
        Boolean, default=False, nullable=False
    )
