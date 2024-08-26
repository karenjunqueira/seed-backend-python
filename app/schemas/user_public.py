from pydantic import BaseModel

class UserPublic(BaseModel):
    username: str | None = None
    email: str