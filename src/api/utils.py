from typing import Callable, Awaitable, Any

from logging import getLogger

from fastapi import Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from security import decode_jwt, JWTBearer
from src.api.session import get_session
from src.db.schemas import User
from src.db.crud import get_user_by_id, get_service_account_by_id

AsyncCallable = Callable[..., Awaitable]
logger = getLogger()


async def service_required(session: AsyncSession, token: str) -> User:
    data = decode_jwt(token)
    if data['type'] != 'service':
        raise HTTPException(status_code=403)
    service = await get_service_account_by_id(session, data['id'])
    if not service:
        raise HTTPException(status_code=403)


async def admin_required(token: str = Depends(JWTBearer()), session: AsyncSession = Depends(get_session)):
    data = decode_jwt(token)
    if data['type'] != 'user':
        raise HTTPException(status_code=403)
    user = await get_user_by_id(session, data['id'])
    if not user.is_admin:
        raise HTTPException(status_code=403, detail="Admin required")


async def user_required(token: str = Depends(JWTBearer()), session: AsyncSession = Depends(get_session)):
    data = decode_jwt(token)
    if data['type'] != 'user':
        raise HTTPException(status_code=403)
    user = await get_user_by_id(session, data['id'])
    if not user:
        raise HTTPException(status_code=403)
