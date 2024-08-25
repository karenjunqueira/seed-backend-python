from pydantic import BaseModel, EmailStr
from bson.objectid import ObjectId

class User(BaseModel):
    _id: ObjectId
    username: str
    email: EmailStr
    password: str
