from typing import Optional
from pydantic import BaseModel, ConfigDict, EmailStr, Field
from bson import ObjectId
from utils.pydantic_objectid import PydanticObjectId

class User(BaseModel):
    _id: Optional[PydanticObjectId]
    username: str | None = None
    email: EmailStr
    password: str | None = None

    model_config = ConfigDict(
        arbitrary_types_allowed = True,
        json_encoders={
            ObjectId: str
        }
    )
