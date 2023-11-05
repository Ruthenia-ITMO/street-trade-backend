import asyncio
from asyncio import WindowsSelectorEventLoopPolicy

from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

import utils
from session import get_session, engine
from security import verify_password, sign_jwt, JWTBearer, get_hash_password
from src.db import schemas, crud
import models

app = FastAPI()

async def admin_required(token: str = Depends(JWTBearer()), session: AsyncSession = Depends(get_session)):
    user = await utils.get_user_from_jwt(session, token)
    if not user.is_admin:
        raise HTTPException(status_code=403, detail="Admin required")



@app.on_event("startup")
async def init_db():
    async with engine.begin() as conn:
        await conn.run_sync(schemas.Base.metadata.create_all)



@app.post("/login")
async def login(user: models.UserLogin, session: AsyncSession = Depends(get_session)):
    res = await crud.get_user_by_name(session, user.name)
    if res:
        if verify_password(user.password, res.hashed_password):
            return sign_jwt(res.id)
    return {
        "error": "Wrong login details!"
    }


@app.post("/add_user", dependencies=[Depends(admin_required)])
async def add_user(user: models.UserCreate, session: AsyncSession = Depends(get_session)):
    res = await crud.get_user_by_name(session, user.name)
    if res:
        return {
            "error": "User already exists!"
        }
    hashed_password = get_hash_password(user.password)
    res = await crud.add_user(session, user.name, hashed_password, user.is_admin)
    return res


@app.get("/")
async def root():
    return {"message": "Hello World"}

if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0")