import time
from typing import Dict

import jwt
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from passlib.context import CryptContext
from fastapi import Depends, Request, HTTPException

from src.api import config

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

SECRET_KEY = config.SECRET_KEY
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = config.ACCESS_TOKEN_EXPIRE_MINUTES


def verify_password(password: str, hashed_password):
    return pwd_context.verify(password, hashed_password)


def get_hash_password(password: str):
    return pwd_context.hash(password)


def token_response(token: str):
    return {
        "access_token": token
    }


def decode_jwt(token: str) -> dict:
    decoded_token = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
    return decoded_token if decoded_token["expires"] >= time.time() else None


def sign_jwt(id: int, **kwargs) -> Dict[str, str]:
    payload = {
        "id": id,
        "expires": time.time() + ACCESS_TOKEN_EXPIRE_MINUTES * 60
    }
    payload.update(kwargs)
    token = jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)

    return token_response(token)


def verify_jwt(jwtoken: str) -> bool:
    isTokenValid: bool = False
    try:
        payload = decode_jwt(jwtoken)
    except jwt.DecodeError:
        payload = None
    if payload:
        isTokenValid = True
    return isTokenValid


class JWTBearer(HTTPBearer):
    def __init__(self, auto_error: bool = True):
        super(JWTBearer, self).__init__(auto_error=auto_error)

    async def __call__(self, request: Request):
        credentials: HTTPAuthorizationCredentials = await super(JWTBearer, self).__call__(request)
        if credentials:
            if not credentials.scheme == "Bearer":
                raise HTTPException(status_code=403, detail="Invalid authentication scheme.")
            if not verify_jwt(credentials.credentials):
                raise HTTPException(status_code=403, detail="Invalid token or expired token.")
            return credentials.credentials
        else:
            raise HTTPException(status_code=403, detail="Invalid authorization code.")
