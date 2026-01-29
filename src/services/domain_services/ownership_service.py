from src.data.dao.session_dao import SessionDAO
from src.data.dao.block_dao import BlockDAO
from src.data.dao.exercise_dao import ExerciseDAO
import uuid

class OwnershipService:
    def __init__(self, session_dao : SessionDAO, block_dao : BlockDAO, exercise_dao:ExerciseDAO):
        self.session_dao = session_dao
        self.block_dao = block_dao
        self.exercise_dao = exercise_dao

    def check_user_is_owner_session(self, user_id: uuid.UUID, session_id: uuid.UUID) -> None:
        session = self.session_dao.get_by_id(session_id)
        if not session:
            raise ValueError("Session not found")
        if session.user_id != user_id:
            raise PermissionError("User does not have access to this session")
        
    def check_user_is_owner_block(self, user_id: uuid.UUID, block_id: uuid.UUID) -> None:
        block = self.block_dao.get_by_id(block_id)
        if not block:
            raise ValueError("Block not found")
        self.check_user_is_owner_session(user_id, block.session_id)

    def check_user_is_owner_exercise(self, user_id: uuid.UUID, exercise_id: uuid.UUID) -> None:
        exercise = self.exercise_dao.get_by_id(exercise_id)
        if not exercise:
            raise ValueError("Exercise not found")
        self.check_user_is_owner_session(user_id, exercise.session_id)