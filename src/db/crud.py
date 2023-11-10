import secrets

from sqlalchemy import select, Select, func
from sqlalchemy.ext.asyncio import AsyncSession

from src.api.security import get_hash_password
from src.db.schemas import User, Frame, Stream, Service_Account


async def paginate(session: AsyncSession, query: Select, limit: int, offset: int) -> dict:
    return {
        'count': await session.scalar(select(func.count()).select_from(query.subquery())),
        'items': [record for record in await session.scalars(query.limit(limit).offset(offset))]
    }


async def add_user(session: AsyncSession, name: str, hashed_password: str, is_admin: bool) -> User:
    user = User(name=name, hashed_password=hashed_password, is_admin=is_admin)
    session.add(user)
    await session.flush()
    return user


async def get_user_by_id(session: AsyncSession, user_id: int) -> User:
    user = await session.scalars(select(User).where(User.id == user_id))
    return user.first()


async def get_user_by_name(session: AsyncSession, name: str) -> User:
    user = await session.scalars(select(User).where(User.name == name))
    return user.first()


async def add_stream(session, name, rtcp_url, hls_url):
    stream = Stream(name=name, rtsp_url=rtcp_url, hls_url=hls_url)
    session.add(stream)
    await session.flush()
    return stream


async def get_stream_by_name(session, name):
    res = await session.scalars(select(Stream).where(Stream.name == name))
    return res.first()


async def get_streams(session, limit, offset):
    res = await paginate(session, select(Stream), limit, offset)
    return res


async def get_frames(session, limit, offset):
    res = await paginate(session, select(Frame), limit, offset)
    return res


async def get_service_account_by_name(session: AsyncSession, name):
    res = await session.scalars(select(Service_Account).where(Service_Account.name == name))
    return res.first()


async def get_service_account_by_id(session: AsyncSession, id):
    res = await session.scalars(select(Service_Account).where(Service_Account.id == id))
    return res.first()


async def add_service_account(session: AsyncSession, name):
    token = secrets.token_urlsafe(64)
    hashed_token = get_hash_password(token)
    service_account = Service_Account(name=name, hashed_token=hashed_token)
    session.add(service_account)
    await session.flush()
    return {
        "name": name,
        "token": token
    }


async def add_frame_url(session: AsyncSession, frame_url: str, stream_id: id):
    frame = Frame(stream_id=stream_id, frame_url=frame_url)
    session.add(frame)
    await session.flush()


async def set_frame_validity(session, frame_id, is_valid):
    frame = await session.scalars(select(Frame).where(Frame.id == frame_id))
    frame = frame.first()
    frame.is_correct = is_valid
    await session.flush()
