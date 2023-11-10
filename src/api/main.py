import asyncio
import os

from fastapi import FastAPI, Depends, HTTPException, Query
from fastapi.middleware.cors import CORSMiddleware

from src.api.session import get_db_session, engine
from src.api.security import verify_password, sign_jwt, JWTBearer, get_hash_password
from src.api import config
from src.api.routers import user, rtsp, frames, neuro
from src.db import schemas, crud
from src.db.crud import get_user_by_name

app = FastAPI()
app.include_router(user.router)
app.include_router(rtsp.router)
app.include_router(frames.router)
app.include_router(neuro.router)
app.add_middleware(
    CORSMiddleware,
    allow_origins=['*'],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.on_event("startup")
async def init_db():
    async with engine.begin() as conn:
        await conn.run_sync(schemas.Base.metadata.create_all)
    conn = await get_db_session()
    if not await get_user_by_name(conn, 'admin'):
        await crud.add_user(session=conn, name="admin", hashed_password=get_hash_password(config.ADMIN_PASSWORD),
                            is_admin=True)
        await conn.commit()


@app.get("/")
async def root():
    return {"message": "Hello World"}


if __name__ == "__main__":
    import uvicorn

    if os.name == 'nt':
        from asyncio import WindowsSelectorEventLoopPolicy

        asyncio.set_event_loop_policy(WindowsSelectorEventLoopPolicy())
    uvicorn.run(app, host="0.0.0.0")
