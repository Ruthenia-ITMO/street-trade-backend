from pydantic import BaseModel, Field

class UserLogin(BaseModel):
    name: str
    password: str


class UserCreate(BaseModel):
    name: str
    password: str
    is_admin: bool = False
