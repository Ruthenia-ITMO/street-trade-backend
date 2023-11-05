from typing import Callable, Awaitable, Any

from logging import getLogger

from sqlalchemy.ext.asyncio import AsyncSession

from security import decode_jwt
from src.db.schemas import User
from src.db.crud import get_user_by_id

AsyncCallable = Callable[..., Awaitable]
logger = getLogger()


async def get_user_from_jwt(session: AsyncSession, token: str) -> User:
    data = decode_jwt(token)
    user = await get_user_by_id(session, data['user_id'])
    return user
