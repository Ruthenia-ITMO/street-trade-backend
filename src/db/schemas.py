from sqlalchemy import String, ForeignKey, JSON, Column, Integer, Boolean, DateTime
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession
from sqlalchemy.ext.orderinglist import OrderingList, ordering_list
from datetime import datetime


class Base(DeclarativeBase):
    pass


class Service_Account(Base):
    __tablename__ = "service_account"

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String, unique=True, nullable=False, index=True)
    hashed_token = Column(String, nullable=False)


class User(Base):
    __tablename__ = "user"

    id = Column(Integer, primary_key=True, autoincrement=True, index=True)
    name = Column(String, unique=True, nullable=False, index=True)
    hashed_password = Column(String, nullable=False)
    is_admin = Column(Boolean, nullable=False, default=False)


class RTSP_Stream(Base):
    __tablename__ = "RTSP_stream"

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String, unique=True, nullable=False, index=True)
    url = Column(String, nullable=False)
    login = Column(String, nullable=True)
    password = Column(String, nullable=True)

    frames = relationship("Frame", back_populates="stream")


class Frame(Base):
    __tablename__ = "frame"

    id = Column(Integer, primary_key=True, autoincrement=True)
    stream_id = Column(Integer, ForeignKey("RTSP_stream.id"), nullable=False)
    frame_url = Column(String, nullable=False)
    timestamp = Column(DateTime, default=datetime.now())
    is_correct = Column(Boolean, default=True)

    stream = relationship("RTSP_Stream", back_populates="frames")
