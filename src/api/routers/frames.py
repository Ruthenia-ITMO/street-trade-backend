from fastapi import APIRouter, Depends, Query, UploadFile, HTTPException, Form, File
from sqlalchemy.ext.asyncio import AsyncSession

from src.api import config
from src.api.security import JWTBearer, verify_password
from src.api.models import ValidityForm, ServiceAccountUpload
from src.api.session import get_db_session, get_s3_session
from src.api.utils import admin_required, service_required
from src.db import crud
from urllib.parse import urlparse

from datetime import datetime

router = APIRouter(
    prefix="/frames",
    tags=["frames"],
    responses={404: {"description": "Not found"}},
)


@router.get("/", dependencies=[Depends(JWTBearer())])
async def get_frames(session: AsyncSession = Depends(get_db_session), page: int = Query(1, ge=1),
                     per_page: int = Query(100, ge=0)):
    limit = per_page * page
    offset = (page - 1) * per_page
    res = await crud.get_frames(session, limit, offset)
    return res


@router.get('/{id}', dependencies=[Depends(JWTBearer())])
async def get_frame(id: int, session: AsyncSession = Depends(get_db_session)):
    res = await crud.get_frame_by_id(session, id)
    return res


@router.post("/validity", dependencies=[Depends(JWTBearer())])
async def set_correct(data: ValidityForm, session: AsyncSession = Depends(get_db_session)):
    await crud.set_frame_validity(session, data.frame_id, data.is_valid)
    await session.commit()
    return 'ok'


@router.post("/upload")
async def upload_frames(file: UploadFile = File(...), name: str = Form(...), token: str = Form(...), rtsp_id: int = Form(...),
                        session: AsyncSession = Depends(get_db_session),
                        s3=Depends(get_s3_session)):
    form = ServiceAccountUpload(name=name, token=token, rtsp_id=rtsp_id)
    res = await crud.get_service_account_by_name(session, form.name)
    if not verify_password(form.token, res.hashed_token):
        return HTTPException(status_code=401, detail="Wrong login details!")
    rtsp_id = form.rtsp_id
    bucket_name = config.S3_BUCKET
    file_type = file.filename.split(".")[-1]
    file_key = f"{rtsp_id}_{datetime.now().strftime('%Y_%m_%d_%H_%M_%S')}.{file_type}"
    async with s3 as s3_session:
        await s3_session.upload_fileobj(file.file, bucket_name, file_key)
    host = urlparse(config.S3_URL)
    url = f"{host.scheme}://{config.S3_BUCKET}.{host.netloc}/{file_key}"
    await crud.add_frame_url(session, url, rtsp_id)
    await session.commit()
    return {"OK": 200, "url": url}
