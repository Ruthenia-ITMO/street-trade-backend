from fastapi import APIRouter, Depends, Query
from sqlalchemy.ext.asyncio import AsyncSession

from src.api import models
from src.api.security import JWTBearer
from src.api.session import get_session
from src.api.utils import admin_required
from src.db import crud

router = APIRouter(
    prefix="/rtsp",
    tags=["rtsp"],
    responses={404: {"description": "Not found"}},
)


@router.post("/add", dependencies=[Depends(admin_required)])
async def add_RTSP_Stream(camera: models.RTSP_Stream, session: AsyncSession = Depends(get_session)):
    res = await crud.get_RTSP_Stream_by_name(session, camera.name)
    if res:
        return {
            "error": "Camera already exists!"
        }
    res = await crud.add_RTSP_Stream(session, camera.name, camera.url)
    await session.commit()
    return res


@router.get("/get/all", dependencies=[Depends(JWTBearer())])
async def get_RTSP_Streams(session: AsyncSession = Depends(get_session), limit: int = Query(100, ge=0),
                           offset: int = Query(0, ge=0)):
    res = await crud.get_RTSP_Streams(session, limit, offset)
    return res
