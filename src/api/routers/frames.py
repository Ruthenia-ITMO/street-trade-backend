from fastapi import APIRouter, Depends, Query
from sqlalchemy.ext.asyncio import AsyncSession

from src.api.security import JWTBearer
from src.api.session import get_session
from src.api.utils import admin_required, service_required
from src.db import crud

router = APIRouter(
    prefix="/frames",
    tags=["frames"],
    responses={404: {"description": "Not found"}},
)


@router.get("/get/all", dependencies=[Depends(JWTBearer())])
async def get_frames(session: AsyncSession = Depends(get_session), limit: int = Query(100, ge=0),
                     offset: int = Query(0, ge=0)):
    res = await crud.get_frames(session, limit, offset)
    return res

@router.post("/upload", dependencies=[Depends(service_required)])
