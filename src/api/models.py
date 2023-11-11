from pydantic import BaseModel, Field

class UserLogin(BaseModel):
    name: str
    password: str


class UserCreate(BaseModel):
    name: str
    password: str
    is_admin: bool = False


class stream(BaseModel):
    name: str
    rtsp_url: str


class ServiceAccountLogin(BaseModel):
    name: str
    token: str


class ValidityForm(BaseModel):
    frame_id: int
    is_valid: bool

class AddServiceAccount(BaseModel):
    name: str