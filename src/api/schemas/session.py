from datetime import date as d
from pydantic import BaseModel, Field
from src.data.models import SessionType
import uuid

class SessionCreate(BaseModel):
    name: str
    date: d
    session_type: SessionType
    notes: str | None = None
    location_id : uuid.UUID | None = None

class SessionUpdate(BaseModel):
    name: str | None = Field(None, max_length=100)
    date: d | None = None
    session_type: SessionType | None = None
    notes: str | None = None
    location_id : uuid.UUID | None = None

class SessionRead(BaseModel):
    id: uuid.UUID
    name: str
    date: d
    session_type: SessionType
    user_id: uuid.UUID
    notes: str | None = None
    location_id : uuid.UUID | None = None

    class Config:
        from_attributes = True
