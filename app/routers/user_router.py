from http import HTTPStatus
from fastapi import APIRouter, Depends
from fastapi.exceptions import HTTPException
from models.user import User
from schemas.user_request import UserRequest
from schemas.user_response import UserResponse
from services.user_service import UserService
from core.security import get_current_user

router = APIRouter(prefix="/users", tags=["User"])
service = UserService()

@router.get("")    
def get_all():    
    search = service.get_all()
    return search

@router.get("/{user_id}", response_model=UserResponse)    
def read_user(user_id: str):    
    search = service.get_by_id(user_id)
    if search is None:
        raise HTTPException(status_code=404, detail="User not found")
    return search

@router.post("", status_code=HTTPStatus.CREATED, response_model=UserResponse)
def create_user(user: UserRequest):
    new_user = service.create_user(user)
    return new_user

@router.put("/{user_id}")
def update_user(user_id: str, user: UserRequest,
                current_user: User = Depends(get_current_user)):
    if str(current_user.id) != user_id:
        raise HTTPException(
            status_code=HTTPStatus.FORBIDDEN, detail='Not enough permissions'
        )

    new_user = service.update_user(user_id, user)
    if new_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return new_user    

@router.delete("/{user_id}") 
def delete_user(user_id: str,
                current_user: User = Depends(get_current_user)):
    if str(current_user.id) != user_id:
        raise HTTPException(
            status_code=HTTPStatus.FORBIDDEN, detail='Not enough permissions'
        )
    deleted = service.delete_user(user_id)
    return deleted