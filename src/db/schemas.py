from sqlalchemy import String, ForeignKey, JSON, Column, Integer, Boolean, DateTime
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession
from sqlalchemy.ext.orderinglist import OrderingList, ordering_list


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


class RTSP_Stream:
    __tablename__ = "RTSP_stream"

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String, unique=True, nullable=False, index=True)
    url = Column(String, nullable=False)


class Frame:
    __tablename__ = "frame"

    id = Column(Integer, primary_key=True, autoincrement=True)
    stream_id = Column(Integer, ForeignKey("rtsp_stream.id"), nullable=False)
    frame_url = Column(String, nullable=False)
    timestamp = Column(DateTime, nullable=False)

    stream = relationship("RTSP_Stream", back_populates="frames")
