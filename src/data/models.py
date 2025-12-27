from sqlalchemy import (
    Column, Integer, String, ForeignKey, Date, Enum, Float, Text, UniqueConstraint, Index
)
from sqlalchemy.orm import relationship, DeclarativeBase, Mapped, mapped_column
import enum

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

# -------------------
# Models
# -------------------
class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    username: Mapped[str] = mapped_column(String(50), nullable=False, unique=True)

    sessions: Mapped[list["Session"]] = relationship("Session", back_populates="user")


class Session(Base):
    __tablename__ = "sessions"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String(100), nullable=False)
    date: Mapped[Date] = mapped_column(Date, nullable=False)
    session_type: Mapped[SessionType] = mapped_column(Enum(SessionType), nullable=False)
    user_id: Mapped[int] = mapped_column(Integer, ForeignKey("users.id"), index=True)
    notes: Mapped[str | None] = mapped_column(Text, nullable=True)

    user: Mapped["User"] = relationship("User", back_populates="sessions")
    blocks: Mapped[list["Block"]] = relationship("Block", back_populates="session", order_by="Block.position")
    photos: Mapped[list["Photo"]] = relationship("Photo", back_populates="session")


class Block(Base):
    __tablename__ = "blocks"
    __table_args__ = (
        UniqueConstraint('session_id', 'position', name='uix_session_block_position'),
        Index('ix_block_position', 'position'),
    )

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    block_type: Mapped[BlockType] = mapped_column(Enum(BlockType), nullable=False)
    duration: Mapped[float | None] = mapped_column(Float, nullable=True)
    position: Mapped[int] = mapped_column(Integer, nullable=False)
    session_id: Mapped[int] = mapped_column(Integer, ForeignKey("sessions.id"), index=True)
    notes: Mapped[str | None] = mapped_column(Text, nullable=True)

    session: Mapped["Session"] = relationship("Session", back_populates="blocks")
    exercises: Mapped[list["Exercise"]] = relationship("Exercise", back_populates="block", order_by="Exercise.position")


class Exercise(Base):
    __tablename__ = "exercises"
    __table_args__ = (
        UniqueConstraint('block_id', 'position', name='uix_block_exercise_position'),
        Index('ix_exercise_position', 'position'),
    )

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    exercise_type: Mapped[ExerciseType] = mapped_column(Enum(ExerciseType), nullable=False)
    weight_kg: Mapped[float | None] = mapped_column(Float, nullable=True)
    repetitions: Mapped[int | None] = mapped_column(Integer, nullable=True)
    duration_seconds: Mapped[float | None] = mapped_column(Float, nullable=True)
    distance_meters: Mapped[float | None] = mapped_column(Float, nullable=True)
    block_id: Mapped[int] = mapped_column(Integer, ForeignKey("blocks.id"), index=True)
    position: Mapped[int] = mapped_column(Integer, nullable=False)
    notes: Mapped[str | None] = mapped_column(Text, nullable=True)

    block: Mapped["Block"] = relationship("Block", back_populates="exercises")


class Photo(Base):
    __tablename__ = "photos"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    path: Mapped[str] = mapped_column(String(255), nullable=False)
    session_id: Mapped[int] = mapped_column(Integer, ForeignKey("sessions.id"), index=True)
    notes: Mapped[str | None] = mapped_column(Text, nullable=True)

    session: Mapped["Session"] = relationship("Session", back_populates="photos")

