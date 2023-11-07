import asyncio
import os
from asyncio import WindowsSelectorEventLoopPolicy

from fastapi import FastAPI, Depends, HTTPException, Query
from sqlalchemy.ext.asyncio import AsyncSession

import utils
from session import get_session, engine
from security import verify_password, sign_jwt, JWTBearer, get_hash_password
from src.api.routers import user, rtsp, frames, neuro
from src.db import schemas, crud
import models

app = FastAPI()
app.include_router(user.router)
app.include_router(rtsp.router)
app.include_router(frames.router)
app.include_router(neuro.router)


@app.on_event("startup")
async def init_db():
    async with engine.begin() as conn:
        await conn.run_sync(schemas.Base.metadata.create_all)
    # ONLY FOR TESTING
    # conn = await get_session()
    # await crud.add_user(session=conn, name="admin", hashed_password=get_hash_password("admin"), is_admin=True)
    # await conn.commit()




@app.get("/")
async def root():
    return {"message": "Hello World"}


if __name__ == "__main__":
    import uvicorn

    if os.name == 'nt':
        asyncio.set_event_loop_policy(WindowsSelectorEventLoopPolicy())
    uvicorn.run(app, host="0.0.0.0")
