from typing import Union
from fastapi import APIRouter
from fastapi.exceptions import HTTPException
from models.item import Item
from services.item_service import ItemService

router = APIRouter()
service = ItemService()

list_items = {}


@router.get("")    
def get_all():    
    search = service.get_all()
    return search

@router.get("/{item_id}")    
def read_item(item_id: str):    
    search = service.get_by_id(item_id)
    if search is None:
        raise HTTPException(status_code=404, detail="Item not found")
    return search

@router.post("")
def adding_item(item: Item):
    new_item = service.create_item(item)
    return new_item

@router.put("/{item_id}")
def update_item(item_id: str, item: Item):
    new_item = service.update_item(item_id, item)
    if new_item is None:
        raise HTTPException(status_code=404, detail="Item not found")
    return new_item    

@router.delete("/{item_id}") 
def delete_item(item_id: str):
    deleted = service.delete_item(item_id)
    return deleted