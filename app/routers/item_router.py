from typing import Union
from pydantic import BaseModel
from fastapi import APIRouter

router = APIRouter()

class Item(BaseModel):
    id: int
    name: str

list_items = {}

@router.get("/{item_id}")    
def read_item(item_id: int):    
    search = list(filter(lambda x: x == item_id, list_items))

    if search == []:
        return {'Item': 'Not found'}

    return list_items[search[0]]

@router.post("")
def adding_item(item: Item):
    list_items[item.id] = item
    return {"item_name": item.name}

@router.put("/{item_id}")
def update_item(item_id: int, item: Item):
    search = list(filter(lambda x: x == item_id, list_items))

    if search == []:
        return {'Item': 'Not found'}

    list_items[item_id] = item

    return list_items    

@router.delete("/{item_id}") 
def delete_item(item_id: int):
    search = list(filter(lambda x: x == item_id, list_items))

    if search == []:
        return {'Item': 'Not found'}
    
    del list_items[item_id]

    return list_items