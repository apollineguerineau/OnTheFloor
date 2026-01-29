from pydantic import BaseModel
import uuid

class UserCreate(BaseModel):
    username: str
    password: str

class UserLogin(BaseModel):
    username: str
    password: str

class UserRead(BaseModel):
    id: uuid.UUID
    username: str

    model_config = {
        "from_attributes": True
    }