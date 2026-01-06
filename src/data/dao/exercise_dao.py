from sqlalchemy.orm import Session as DBSession
from sqlalchemy import select

from src.data.models import Exercise, Block


class ExerciseDAO:
    def __init__(self, db: DBSession):
        self.db = db

    def create(self, exercise: Exercise) -> Exercise:
        self.db.add(exercise)
        self.db.commit()
        self.db.refresh(exercise)
        return exercise

    def get_by_id(self, exercise_id: int) -> Exercise | None:
        return self.db.get(Exercise, exercise_id)

    def list_by_session(self, session_id: int) -> list[Exercise]:
        # Tri par position dans le block si nécessaire, sinon par position globale
        stmt = (
            select(Exercise)
            .where(Exercise.session_id == session_id)
            .order_by(Exercise.position_in_block, Exercise.position)
        )
        return list(self.db.scalars(stmt))

    def list_by_block(self, block_id: int) -> list[Exercise]:
        stmt = (
            select(Exercise)
            .where(Exercise.block_id == block_id)
            .order_by(Exercise.position)
        )
        return list(self.db.scalars(stmt))

    def update(self, exercise: Exercise) -> Exercise:
        self.db.commit()
        self.db.refresh(exercise)
        return exercise

    def delete(self, exercise: Exercise) -> None:
        self.db.delete(exercise)
        self.db.commit()

    def validate_block_session(self, block_id: int, session_id: int) -> bool:
        block = self.db.get(Block, block_id)
        return block is not None and block.session_id == session_id


