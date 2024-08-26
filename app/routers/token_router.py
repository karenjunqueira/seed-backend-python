from http import HTTPStatus
from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from core.security import (
    create_access_token,
    get_password_hash,
    verify_password,
)
from models.user import User
from schemas.token import Token
from schemas.user_public import UserPublic
from services.user_service import UserService

router = APIRouter(prefix='/auth', tags=['auth'])
service = UserService()


@router.post('/token', response_model=Token)
def login_for_access_token(
    form_data: OAuth2PasswordRequestForm = Depends()
):
    user_public = UserPublic(email=form_data.username)
    users_list = service.get_by_attributes(user_public)

    if len(users_list) == 0:
        raise HTTPException(
            status_code=HTTPStatus.BAD_REQUEST,
            detail='Incorrect email or password'
        )

    if not verify_password(form_data.password, users_list[0].password):
        raise HTTPException(
            status_code=HTTPStatus.BAD_REQUEST,
            detail='Incorrect email or password'
        )

    access_token = create_access_token(data={'sub': users_list[0].email})

    return {'access_token': access_token, 'token_type': 'bearer'}