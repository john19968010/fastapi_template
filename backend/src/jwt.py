from pydantic import BaseModel
from typing import Union
from datetime import datetime, timedelta
from fastapi.security import HTTPBearer
import jwt
from fastapi import Depends
from .exception import TOKEN_COULD_NOT_VALIDATE


######## jwt token ########
ALGORITHM: str = "HS256"
ACCESS_TOKEN_DAY: int = 1
OAUTH2_SCHEMA: HTTPBearer = HTTPBearer()


class TokenSchema(BaseModel):
    id: int
    username: str
    exp: str


def create_access_token(
    data: dict, expires_delta: Union[timedelta, None] = None
) -> str:
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(hours=1)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, "", algorithm=ALGORITHM)
    return encoded_jwt


def get_current_user(token: str = Depends(OAUTH2_SCHEMA)) -> dict[str, str]:
    try:
        payload: dict = jwt.decode(token.credentials, "", algorithms=ALGORITHM)
        ret = {
            "uuid": payload.get("uuid"),
            "type": payload.get("type"),
            "name": payload.get("name"),
            "is_admin": payload.get("is_admin"),
        }
        if not ret:
            raise TOKEN_COULD_NOT_VALIDATE

    except jwt.PyJWTError:
        raise TOKEN_COULD_NOT_VALIDATE

    return ret
