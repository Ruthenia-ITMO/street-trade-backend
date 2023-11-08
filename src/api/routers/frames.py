from fastapi import APIRouter, Depends, Query, UploadFile
from sqlalchemy.ext.asyncio import AsyncSession

from src.api.security import JWTBearer
from src.api.session import get_session
from src.api.utils import admin_required, service_required
from src.db import crud

from datetime import datetime

from src.api.config import s3, required_env

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
async def upload_frames(rtsp_id: int, file: UploadFile, session: AsyncSession = Depends(get_session)):
    bucket_name = "aboba"
    file_type = file.filename.split(".")[-1]
    file_key = f"{rtsp_id}_{datetime.now().strftime('%Y_%m_%d_%H_%M_%S')}.{file_type}"
    s3.meta.client.upload_fileobj(file.file, bucket_name, file_key)
    url = f"{required_env('S3_URL')}/{bucket_name}/{file_key}"
    await crud.add_frame_url(session, url, rtsp_id)
    await session.commit()
    return {"OK": 200, "url": url}
