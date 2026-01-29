from sqlalchemy import select, func
from sqlalchemy.engine import Engine
import uuid

from src.data.models import Exercise, Block
from src.core.database import new_session
from src.core.entities import ExerciseEntity


class ExerciseDAO:
    def __init__(self, engine: Engine):
        self.engine = engine

    def create(self, exercise_entity: ExerciseEntity) -> uuid.UUID:
        with new_session(self.engine) as session:
            exercise_model = Exercise(
                session_id=exercise_entity.session_id,
                block_id=exercise_entity.block_id,
                exercise_type=exercise_entity.exercise_type,
                weight_kg=exercise_entity.weight_kg,
                repetitions=exercise_entity.repetitions,
                duration_seconds=exercise_entity.duration_seconds,
                distance_meters=exercise_entity.distance_meters,
                notes=exercise_entity.notes,
                position=exercise_entity.position,
                position_in_block=exercise_entity.position_in_block,
            )
            session.add(exercise_model)
            session.commit()
            session.refresh(exercise_model)
            return exercise_model.id

    def get_by_id(self, exercise_id: uuid.UUID) -> ExerciseEntity | None:
        with new_session(self.engine) as session:
            model = session.get(Exercise, exercise_id)
            return model.to_entity() if model else None

    def list_by_session(self, session_id: uuid.UUID) -> list[ExerciseEntity]:
        stmt = (
            select(Exercise)
            .where(Exercise.session_id == session_id)
            .order_by(Exercise.position_in_block, Exercise.position)
        )
        with new_session(self.engine) as session:
            models = session.scalars(stmt).all()
            return [m.to_entity() for m in models]

    def list_by_block(self, block_id: uuid.UUID) -> list[ExerciseEntity]:
        stmt = (
            select(Exercise)
            .where(Exercise.block_id == block_id)
            .order_by(Exercise.position)
        )
        with new_session(self.engine) as session:
            models = session.scalars(stmt).all()
            return [m.to_entity() for m in models]

    def delete(self, exercise_id: uuid.UUID) -> None:
        with new_session(self.engine) as session:
            model = session.get(Exercise, exercise_id)
            if model:
                session.delete(model)
                session.commit()

    def validate_block_session(self, block_id: uuid.UUID, session_id: uuid.UUID) -> bool:
        with new_session(self.engine) as session:
            block = session.get(Block, block_id)
            return block is not None and block.session_id == session_id

    def count_free_by_session(self, session_id: uuid.UUID) -> int:
        with new_session(self.engine) as session:
            return session.scalar(
                select(func.count())
                .select_from(Exercise)
                .where(
                    Exercise.session_id == session_id,
                    Exercise.block_id.is_(None),
                )
            )

    def count_by_block(self, block_id: uuid.UUID) -> int:
        with new_session(self.engine) as session:
            return session.scalar(
                select(func.count())
                .select_from(Exercise)
                .where(Exercise.block_id == block_id)
            )
