from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from src.api import models
from src.api.security import get_hash_password, verify_password, sign_jwt
from src.api.session import get_session
from src.api.utils import admin_required
from src.db import crud

router = APIRouter(
    prefix="/user",
    tags=["user"],
    responses={404: {"description": "Not found"}},
)


@router.post("/login")
async def login(user: models.UserLogin, session: AsyncSession = Depends(get_session)):
    res = await crud.get_user_by_name(session, user.name)
    if res:
        if verify_password(user.password, res.hashed_password):
            return sign_jwt(res.id, type='user')
    raise HTTPException(status_code=401, detail="Wrong login details!")


@router.post("/add", dependencies=[Depends(admin_required)])
async def add_user(user: models.UserCreate, session: AsyncSession = Depends(get_session)):
    res = await crud.get_user_by_name(session, user.name)
    if res:
        return {
            "error": "User already exists!"
        }
    hashed_password = get_hash_password(user.password)
    res = await crud.add_user(session, user.name, hashed_password, user.is_admin)
    # TODO Create middleware to commit session
    await session.commit()
    return res.name
