from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession

from src.api import config
from aioboto3 import Session

engine = create_async_engine(config.DB_URL, echo=True)
async_session: async_sessionmaker = async_sessionmaker(engine, expire_on_commit=False)


async def get_db_session() -> AsyncSession:
    async with async_session() as session:
        async with session.begin():
            return session


async def get_s3_session() -> Session:
    session = Session()
    client = session.client('s3', endpoint_url=config.S3_URL, aws_access_key_id=config.S3_ACCESS_KEY,
                              aws_secret_access_key=config.S3_SECRET_ACCESS_KEY)
    return client
