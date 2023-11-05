from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from src.db.schemas import User


async def add_user(db: AsyncSession, name: str, hashed_password: str, is_admin: bool) -> User:
    user = User(name=name, hashed_password=hashed_password, is_admin=is_admin)
    db.add(user)
    await db.flush()
    return user


async def get_user_by_id(session: AsyncSession, user_id: int) -> User:
    user = await session.scalars(select(User).where(User.id == user_id))
    return user.first()


async def get_user_by_name(session: AsyncSession, name: str) -> User:
    user = await session.scalars(select(User).where(User.name == name))
    return user.first()
