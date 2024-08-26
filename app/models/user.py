from pydantic import BaseModel, EmailStr
from bson.objectid import ObjectId

class User(BaseModel):
    _id: ObjectId | None = None
    username: str | None = None
    email: EmailStr
    password: str | None = None
