from pydantic import BaseModel
from bson.objectid import ObjectId

class Item(BaseModel):
    _id: ObjectId
    id: int
    name: str
