from pydantic import BaseModel

class UserRequest(BaseModel):
    username: str | None = None
    email: str | None = None
    password: str | None = None