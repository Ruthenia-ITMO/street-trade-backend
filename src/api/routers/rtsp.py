import uuid
from urllib.parse import urlparse

from fastapi import APIRouter, Depends, Query
from sqlalchemy.ext.asyncio import AsyncSession
import httpx

from src.api import models, config
from src.api.security import JWTBearer
from src.api.session import get_db_session
from src.api.utils import admin_required
from src.db import crud

router = APIRouter(
    prefix="/streams",
    tags=["streams"],
    responses={404: {"description": "Not found"}},
)


@router.post("/add", dependencies=[Depends(admin_required)])
async def add_stream(camera: models.stream, session: AsyncSession = Depends(get_db_session)):
    res = await crud.get_stream_by_name(session, camera.name)
    if res:
        return {
            "error": "Camera already exists!"
        }
    rnd_id = uuid.uuid4()
    async with httpx.AsyncClient() as client:
        _ = await client.post(config.RTSPTOWEB_URL + f'/stream/{rnd_id}/add', json={
            "name": "test video",
            "channels": {
                "0": {
                    "name": "0",
                    "url": camera.rtsp_url,
                    "on_demand": True,
                    "debug": False,
                    "status": 0
                },
            }
        })
    res = await crud.add_stream(session, camera.name, camera.rtsp_url,
                                config.RTSPTOWEB_URL + f'/stream/{rnd_id}/channel/0/hls/live/index.m3u8')
    await session.commit()
    return res


@router.get("/", dependencies=[Depends(JWTBearer())])
async def get_streams(session: AsyncSession = Depends(get_db_session), page: int = Query(1, ge=1),
                      per_page: int = Query(100, ge=0)):
    limit = per_page * page
    offset = (page - 1) * per_page
    res = await crud.get_streams(session, limit, offset)
    return res

@router.get('/{id}', dependencies=[Depends(JWTBearer())])
async def get_stream(id: int, session: AsyncSession = Depends(get_db_session)):
    res = await crud.get_stream_by_id(session, id)
    return res
