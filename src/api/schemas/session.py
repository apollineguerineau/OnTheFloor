from datetime import date as d
from pydantic import BaseModel, Field
from src.data.models import SessionType

class SessionCreate(BaseModel):
    name: str
    date: d
    session_type: SessionType
    user_id: int
    notes: str | None = None
    location_id : int | None = None

class SessionUpdate(BaseModel):
    name: str | None = Field(None, max_length=100)
    date: d | None = None
    session_type: SessionType | None = None
    notes: str | None = None
    location_id : int | None = None

class SessionRead(BaseModel):
    id: int
    name: str
    date: d
    session_type: SessionType
    user_id: int
    notes: str | None = None
    location_id : int | None = None

    class Config:
        from_attributes = True
