from pydantic import BaseModel
from typing import Optional
from src.data.models import ExerciseType
import uuid


class ExerciseCreate(BaseModel):
    exercise_type: ExerciseType
    session_id: uuid.UUID
    weight_kg: Optional[float] = None
    repetitions: Optional[int] = None
    duration_seconds: Optional[float] = None
    distance_meters: Optional[float] = None
    block_id: Optional[uuid.UUID] = None
    position: Optional[int] = None
    position_in_block: Optional[int] = None
    notes: Optional[str] = None


class ExerciseUpdate(BaseModel):
    exercise_type: Optional[ExerciseType] = None
    weight_kg: Optional[float] = None
    repetitions: Optional[int] = None
    duration_seconds: Optional[float] = None
    distance_meters: Optional[float] = None
    position: Optional[int] = None
    position_in_block: Optional[int] = None
    notes: Optional[str] = None


class ExerciseRead(BaseModel):
    id: uuid.UUID
    exercise_type: ExerciseType
    session_id: uuid.UUID
    weight_kg: Optional[float] = None
    repetitions: Optional[int] = None
    duration_seconds: Optional[float] = None
    distance_meters: Optional[float] = None
    block_id: Optional[uuid.UUID] = None
    position: Optional[int] = None
    position_in_block: Optional[int] = None
    notes: Optional[str] = None

    class Config:
        from_attributes = True
