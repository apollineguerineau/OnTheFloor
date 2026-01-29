from dataclasses import dataclass
import uuid
from datetime import date
from src.data.models import ExerciseType
from src.data.models import BlockType
from src.data.models import LocationType
from src.data.models import SessionType


@dataclass(slots=True)
class UserEntity:
    id: uuid.UUID
    username: str
    hashed_password: str

from dataclasses import dataclass
import uuid
from src.data.models import LocationType


@dataclass(slots=True)
class LocationEntity:
    id: uuid.UUID
    name: str
    address: str | None
    location_type: LocationType


@dataclass(slots=True)
class SessionEntity:
    id: uuid.UUID
    user_id: uuid.UUID
    location_id: uuid.UUID | None
    name: str
    date: date
    session_type: SessionType
    notes: str | None = None


@dataclass(slots=True)
class BlockEntity:
    id: uuid.UUID
    session_id: uuid.UUID
    block_type: BlockType
    position: int
    duration: float | None = None
    notes: str | None = None


@dataclass(slots=True)
class ExerciseEntity:
    id: uuid.UUID
    session_id: uuid.UUID
    block_id: uuid.UUID | None
    exercise_type: ExerciseType

    weight_kg: float | None = None
    repetitions: int | None = None
    duration_seconds: float | None = None
    distance_meters: float | None = None
    notes: str | None = None

    position: int | None = None
    position_in_block: int | None = None