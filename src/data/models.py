from sqlalchemy import (
    Integer,
    String,
    ForeignKey,
    Date,
    Enum,
    Float,
    Text,
    UniqueConstraint,
    Index,
)
from sqlalchemy.orm import relationship, DeclarativeBase, Mapped, mapped_column
import enum
import uuid
from sqlalchemy.dialects.postgresql import UUID

# -------------------
# Base declarative
# -------------------
class Base(DeclarativeBase):
    pass

# -------------------
# Enum types
# -------------------
class SessionType(str, enum.Enum):
    wod = "WOD"
    gym = "Gymnastic"
    weightlifting = "Weightlifting"
    fbb = "Functional Body Building"
    compet = "Competition"
    hyrox = "Hyrox"
    open = "Open"
    team = "Team WOD"


class BlockType(str, enum.Enum):
    amrap = "AMRAP"
    emom = "EMOM"
    for_time = "For Time"
    metcon = "Metcon"
    skill = "Skill/Strength"


class ExerciseType(str, enum.Enum):
    air_squat = "Air Squat"
    back_squat = "Back Squat"
    bear_complex = "Bear Complex"
    bear_walk = "Bear Walk"
    box_jump = "Box Jump"
    broad_jump = "Broad Jump"
    burpee = "Burpee"
    burpee_pull_up = "Burpee-Pull Up"
    chest_to_bar = "Chest to Bar"
    chin_up = "Chin Up"
    clean = "Clean"
    deadlift = "Deadlift"
    devil_press = "Devil Press"
    dip = "Dip"
    double_under = "Double Under"
    front_squat = "Front Squat"
    hand_release_push_up = "Hand Release Push Up"
    handstand_push_up = "Handstand Push-Up"
    hollow_rock = "Hollow Rock"
    jumping_jacks = "Jumping Jacks"
    jumping_lunges = "Jumping Lunges"
    kettlebell_snatch = "Kettlebell Snatch"
    kettlebell_swing = "Kettlebell Swing"
    knees_to_elbows = "Knees to Elbows"
    lunge = "Lunge"
    man_maker = "Man Maker"
    medicine_ball_clean = "Medicine Ball Clean"
    mountain_climber = "Mountain Climber"
    muscle_up = "Muscle Up"
    overhead_squat = "Overhead Squat"
    overhead_walking_lunge = "Overhead Walking Lunge"
    pistol_squat = "Pistol Squat"
    plank = "Plank"
    pull_up = "Pull Up"
    push_jerk = "Push Jerk"
    push_press = "Push Press"
    push_up = "Push Up"
    shoulder_press = "Shoulder Press"
    sit_up = "Sit Up"
    snatch = "Snatch"
    squat = "Squat"
    step_up = "Step Up"
    sumo_deadlift_high_pull = "Sumo Deadlift High Pull"
    superman = "Superman"
    thruster = "Thruster"
    toes_to_bar = "Toes to Bar"
    tuck_jump = "Tuck Jump"
    v_up = "V-up"
    wall_ball = "Wall Balls"
    wall_walk = "Wall Walk"


class LocationType(str, enum.Enum):
    crossfit = "CrossFit Box"
    gym = "Gym"
    none = "None"

# -------------------
# Models
# -------------------
class User(Base):
    __tablename__ = "users"

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4,
    )
    username: Mapped[str] = mapped_column(String(50), nullable=False, unique=True)

    sessions: Mapped[list["Session"]] = relationship(
        "Session",
        back_populates="user",
        cascade="all, delete-orphan",
    )

    hashed_password: Mapped[str] = mapped_column(
        String(255),
        nullable=False,
    )


class Location(Base):
    __tablename__ = "locations"

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4,
    )
    name: Mapped[str] = mapped_column(String(100), nullable=False)
    address: Mapped[str | None] = mapped_column(String(255), nullable=True)
    location_type: Mapped[LocationType] = mapped_column(
        Enum(LocationType),
        nullable=False,
    )

    sessions: Mapped[list["Session"]] = relationship(
        "Session",
        back_populates="location",
    )


class Session(Base):
    __tablename__ = "sessions"

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4,
    )

    user_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("users.id"),
        nullable=False,
        index=True,
    )

    location_id: Mapped[uuid.UUID | None] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("locations.id"),
        nullable=True,
        index=True,
    )

    name: Mapped[str] = mapped_column(String(100), nullable=False)
    date: Mapped[Date] = mapped_column(Date, nullable=False)
    session_type: Mapped[SessionType] = mapped_column(
        Enum(SessionType),
        nullable=False,
    )
    
    notes: Mapped[str | None] = mapped_column(Text, nullable=True)

    user: Mapped["User"] = relationship(
        "User",
        back_populates="sessions",
    )

    location: Mapped["Location | None"] = relationship(
        "Location",
        back_populates="sessions",
    )

    blocks: Mapped[list["Block"]] = relationship(
        "Block",
        back_populates="session",
        order_by="Block.position",
        cascade="all, delete-orphan",
    )

    exercises: Mapped[list["Exercise"]] = relationship(
        "Exercise",
        back_populates="session",
        order_by="Exercise.position",
        cascade="all, delete-orphan",
    )

    photos: Mapped[list["Photo"]] = relationship(
        "Photo",
        back_populates="session",
        cascade="all, delete-orphan",
    )


class Block(Base):
    __tablename__ = "blocks"

    __table_args__ = (
        UniqueConstraint(
            "session_id",
            "position",
            name="uix_session_block_position",
        ),
        Index("ix_block_position", "position"),
    )

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4,
    )

    session_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("sessions.id"),
        nullable=False,
        index=True,
    )

    block_type: Mapped[BlockType] = mapped_column(
        Enum(BlockType),
        nullable=False,
    )
    duration: Mapped[float | None] = mapped_column(Float, nullable=True)
    position: Mapped[int] = mapped_column(Integer, nullable=False)

    notes: Mapped[str | None] = mapped_column(Text, nullable=True)

    session: Mapped["Session"] = relationship(
        "Session",
        back_populates="blocks",
    )

    exercises: Mapped[list["Exercise"]] = relationship(
        "Exercise",
        back_populates="block",
        order_by="Exercise.position",
        cascade="all, delete-orphan",
    )


class Exercise(Base):
    __tablename__ = "exercises"

    __table_args__ = (
        Index("ix_exercise_block_position", "block_id", "position_in_block"),
        Index("ix_exercise_session_position", "session_id", "position"),
    )

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4,
    )

    session_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("sessions.id"),
        nullable=False,
        index=True,
    )

    block_id: Mapped[uuid.UUID | None] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("blocks.id"),
        nullable=True,
        index=True,
    )

    exercise_type: Mapped[ExerciseType] = mapped_column(
        Enum(ExerciseType),
        nullable=False,
    )

    weight_kg: Mapped[float | None] = mapped_column(Float, nullable=True)
    repetitions: Mapped[int | None] = mapped_column(Integer, nullable=True)
    duration_seconds: Mapped[float | None] = mapped_column(Float, nullable=True)
    distance_meters: Mapped[float | None] = mapped_column(Float, nullable=True)

    notes: Mapped[str | None] = mapped_column(Text, nullable=True)

    position: Mapped[int | None] = mapped_column(
        Integer,
        nullable=True,
        comment="Position in session timeline (only for free exercises)",
    )

    position_in_block: Mapped[int | None] = mapped_column(
        Integer,
        nullable=True,
        comment="Position inside a block (only if block_id is not null)",
    )

    session: Mapped["Session"] = relationship(
        "Session",
        back_populates="exercises",
    )

    block: Mapped["Block | None"] = relationship(
        "Block",
        back_populates="exercises",
    )

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        if self.block_id is not None and self.position is not None:
            raise ValueError(
                "An exercise cannot have both position and position_in_block"
            )

        if self.block_id is None and self.position_in_block is not None:
            raise ValueError(
                "Free exercise cannot have position_in_block"
            )


class Photo(Base):
    __tablename__ = "photos"

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4,
    )

    path: Mapped[str] = mapped_column(String(255), nullable=False)

    session_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("sessions.id"),
        nullable=False,
        index=True,
    )

    notes: Mapped[str | None] = mapped_column(Text, nullable=True)

    session: Mapped["Session"] = relationship(
        "Session",
        back_populates="photos",
    )
