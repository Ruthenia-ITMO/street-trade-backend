from fastapi import APIRouter, Depends, HTTPException, Body
from sqlalchemy.ext.asyncio import AsyncSession

from src.api import utils, models
from src.api.models import AddServiceAccount
from src.api.security import verify_password, sign_jwt
from src.api.session import get_db_session
from src.db import crud

router = APIRouter(
    prefix="/services",
    tags=["services"],
    responses={404: {"description": "Not found"}},
)


@router.post("/add", dependencies=[Depends(utils.admin_required)])
async def add_service_account(form: AddServiceAccount, session: AsyncSession = Depends(get_db_session)):
    res = await crud.get_service_account_by_name(session, form.name)
    if res:
        return {
            "error": "Service account already exists!"
        }
    res = await crud.add_service_account(session, form.name)
    await session.commit()
    return res

# @router.post('/login')
# async def login(service_account: models.ServiceAccountLogin, session: AsyncSession = Depends(get_db_session)):
#     res = await crud.get_service_account_by_name(session, service_account.name)
#     if verify_password(service_account.token, res.hashed_token):
#         return sign_jwt(res.id, type='service')
#     raise HTTPException(status_code=401, detail="Wrong login details!")
