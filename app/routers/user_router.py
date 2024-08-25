from typing import Union
from fastapi import APIRouter
from fastapi.exceptions import HTTPException
from models.user import User
from services.user_service import UserService

router = APIRouter()
service = UserService()

@router.get("")    
def get_all():    
    search = service.get_all()
    return search

@router.get("/{user_id}")    
def read_user(user_id: str):    
    search = service.get_by_id(user_id)
    if search is None:
        raise HTTPException(status_code=404, detail="User not found")
    return search

@router.post("")
def adding_user(user: User):
    new_user = service.create_user(user)
    return new_user

@router.put("/{user_id}")
def update_user(user_id: str, user: User):
    new_user = service.update_user(user_id, user)
    if new_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return new_user    

@router.delete("/{user_id}") 
def delete_user(user_id: str):
    deleted = service.delete_user(user_id)
    return deleted