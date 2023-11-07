from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession

from src.api import config

engine = create_async_engine(config.DB_URL, echo=True)
async_session: async_sessionmaker = async_sessionmaker(engine, expire_on_commit=False)



async def get_session() -> AsyncSession:
    async with async_session() as session:
        async with session.begin():
            return session

