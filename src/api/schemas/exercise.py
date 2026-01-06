from pydantic import BaseModel
from typing import Optional
from src.data.models import ExerciseType


class ExerciseCreate(BaseModel):
    exercise_type: ExerciseType
    session_id: int
    weight_kg: Optional[float] = None
    repetitions: Optional[int] = None
    duration_seconds: Optional[float] = None
    distance_meters: Optional[float] = None
    block_id: Optional[int] = None
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
    id: int
    exercise_type: ExerciseType
    session_id: int
    weight_kg: Optional[float] = None
    repetitions: Optional[int] = None
    duration_seconds: Optional[float] = None
    distance_meters: Optional[float] = None
    block_id: Optional[int] = None
    position: Optional[int] = None
    position_in_block: Optional[int] = None
    notes: Optional[str] = None

    class Config:
        from_attributes = True
