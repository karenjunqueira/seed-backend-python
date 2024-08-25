from datetime import datetime, timedelta
from http import HTTPStatus
from fastapi import Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer
from jwt import DecodeError, decode, encode
from zoneinfo import ZoneInfo
from models.user import User
from utils.password_util import PasswordUtil
from schemas.user_public import UserPublic
from services.user_service import UserService

SECRET_KEY = 'your-secret-key'
ALGORITHM = 'HS256'
ACCESS_TOKEN_EXPIRE_MINUTES = 30
oauth2_scheme = OAuth2PasswordBearer(tokenUrl='auth/token')
userService = UserService()


def create_access_token(data: dict):
    to_encode = data.copy()
    expire = datetime.now(tz=ZoneInfo('UTC')) + timedelta(
        minutes=ACCESS_TOKEN_EXPIRE_MINUTES
    )
    to_encode.update({'exp': expire})
    encoded_jwt = encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

def get_password_hash(password: str):
    return PasswordUtil.get_password_hash(password)

def verify_password(plain_password: str, hashed_password: str):
    return PasswordUtil.verify_password(plain_password, hashed_password)


def get_current_user(
    token: str = Depends(oauth2_scheme),
):
    credentials_exception = HTTPException(
        status_code=HTTPStatus.UNAUTHORIZED,
        detail='Could not validate credentials',
        headers={'WWW-Authenticate': 'Bearer'},
    )

    try:
        payload = decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get('sub')

        if not username:
            raise credentials_exception
    except DecodeError:
        raise credentials_exception

    user_public = User(email=username)
    users_list = userService.get_by_attributes(user_public)

    if len(users_list) == 0:
        raise credentials_exception

    return users_list[0]