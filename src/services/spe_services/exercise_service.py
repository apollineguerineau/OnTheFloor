
from src.data.dao.exercise_dao import ExerciseDAO
from src.data.dao.block_dao import BlockDAO
from src.data.models import Exercise, Block
import uuid
from src.services.domain_services.ownership_service import OwnershipService
from src.api.schemas.exercise import ExerciseCreate,ExerciseUpdate


class ExerciseService:
    def __init__(self, exercise_dao : ExerciseDAO, block_dao : BlockDAO, ownership_service : OwnershipService):
        """
        Initialize the ExerciseService with DAOs for exercises and blocks.
        """
        self.exercise_dao = exercise_dao
        self.block_dao = block_dao
        self.ownership_service = ownership_service

    def list_by_session(self, session_id: uuid.UUID, user_id : uuid.UUID) -> list[Exercise]:
        """
        List all exercises in a session, ordered by their global position.
        """
        self.ownership_service.check_user_is_owner_session(user_id=user_id, session_id=session_id)
        return self.exercise_dao.list_by_session(session_id)

    def list_by_block(self, block_id: uuid.UUID, user_id : uuid.UUID) -> list[Exercise]:
        """
        List all exercises in a specific block, ordered by position_in_block.
        """
        self.ownership_service.check_user_is_owner_block(user_id=user_id, block_id=block_id)
        return self.exercise_dao.list_by_block(block_id)

    def get_exercise(self, exercise_id: uuid.UUID, user_id : uuid.UUID) -> Exercise | None:
        """
        Retrieve a single exercise by ID.
        Returns None if not found.
        """
        self.ownership_service.check_user_is_owner_exercise(user_id=user_id, exercise_id=exercise_id)
        return self.exercise_dao.get_by_id(exercise_id)

    # -------------------------
    # Create
    # -------------------------
    def create_exercise(
        self,
        exercise_create : ExerciseCreate,
        user_id : uuid.UUID
    ) -> Exercise:
        """
        Create a new exercise either in a block or as a free exercise in the session.
        Handles automatic position assignment and shifts existing exercises/blocks if needed.
        """
        if exercise_create.session_id is None:
            raise ValueError("Exercise must belong to a session")
        
        self.ownership_service.check_user_is_owner_session(user_id=user_id, session_id=exercise_create.session_id)

        # Validate block ownership
        if exercise_create.block_id is not None and not self.exercise_dao.validate_block_session(exercise_create.block_id, exercise_create.session_id):
            raise ValueError("Block does not belong to the same session")

        if exercise_create.block_id is not None and position is not None:
            raise ValueError("Cannot specify global position for an exercise inside a block")

        # -------------------------
        # Handle positions
        # -------------------------
        if exercise_create.block_id is not None:
            total = self.exercise_dao.count_by_block(exercise_create.block_id)
            # Auto-assign position_in_block if not provided
            if position_in_block is None:
                position_in_block = total
            else:
                if position_in_block < 0 or position_in_block > total:
                    raise ValueError("Invalid position_in_block")
                # Shift existing exercises in the block to make room
                for ex in sorted(
                    self.exercise_dao.list_by_block(exercise_create.block_id),
                    key=lambda e: e.position_in_block or 0,
                    reverse=True
                ):
                    pos = ex.position_in_block or 0
                    if pos >= position_in_block:
                        ex.position_in_block = pos + 1
                        self.exercise_dao.update(ex)
        else:
            total_items = (
                        self.block_dao.count_by_session(exercise_create.session_id)
                        + self.exercise_dao.count_free_by_session(exercise_create.session_id)
                    )
            # Free exercise in session
            if position is None:
                position = total_items
            else : 
                if position < 0 or position > total_items:
                    raise ValueError("Invalid exercise position")
                items_to_shift = [
                    ex for ex in self.exercise_dao.list_by_session(exercise_create.session_id) if ex.position is not None
                ] + self.block_dao.list_by_session(exercise_create.session_id)
                for item in sorted(items_to_shift, key=lambda e: e.position or 0, reverse=True):
                    pos = item.position or 0
                    if pos >= position:
                        item.position = pos + 1
                        if isinstance(item, Exercise):
                            self.exercise_dao.update(item)
                        elif isinstance(item, Block):
                            self.block_dao.update(item)

        # Create the exercise
        exercise = Exercise(
            exercise_type=exercise_create.exercise_type,
            session_id=exercise_create.session_id,
            block_id=exercise_create.block_id,
            position_in_block=position_in_block,
            position=position,
            weight_kg=exercise_create.weight_kg,
            repetitions=exercise_create.repetitions,
            duration_seconds=exercise_create.duration_seconds,
            distance_meters=exercise_create.distance_meters,
            notes=exercise_create.notes,
        )
        return self.exercise_dao.create(exercise)

    # -------------------------
    # Update
    # -------------------------
    def update_exercise(
        self,
        exercise_id: uuid.UUID,
        user_id : uuid.UUID,
        exercise_update : ExerciseUpdate
    ) -> Exercise:
        """
        Update an exercise's properties.
        Position changes within a block or global session are handled properly by shifting others.
        Note: block_id cannot be changed; to move to another block, delete and recreate the exercise.
        """
        self.ownership_service.check_user_is_owner_exercise(user_id=user_id, exercise_id=exercise_id)
        exercise = self.exercise_dao.get_by_id(exercise_id)
        if not exercise:
            raise ValueError("Exercise not found")

        session_id = exercise.session_id
        block_id = exercise.block_id
        old_pos_in_block = exercise.position_in_block or 0
        old_pos = exercise.position or 0

        if block_id is not None and exercise_update.position is not None:
            raise ValueError("Cannot move an exercise out of its block. Delete and create a new one.")

        # -------------------------
        # Update position_in_block
        # -------------------------
        if exercise_update.position_in_block is not None and exercise_update.position_in_block != old_pos_in_block:
            if block_id is not None : 
                total = self.exercise_dao.count_by_block(block_id) - 1
                if exercise_update.position_in_block < 0 or exercise_update.position_in_block > total:
                    raise ValueError("Invalid position_in_block")
                for ex in sorted(
                    (ex for ex in self.exercise_dao.list_by_session(session_id)
                    if ex.id != exercise.id and ex.block_id == block_id),
                    key=lambda e: e.position_in_block or 0,
                    reverse=old_pos_in_block > exercise_update.position_in_block
                ):
                    pos = ex.position_in_block or 0
                    if old_pos_in_block < exercise_update.position_in_block and old_pos_in_block < pos <= exercise_update.position_in_block:
                        ex.position_in_block = pos - 1
                    elif old_pos_in_block > exercise_update.position_in_block and exercise_update.position_in_block <= pos < old_pos_in_block:
                        ex.position_in_block = pos + 1
                    self.exercise_dao.update(ex)
                exercise.position_in_block = exercise_update.position_in_block

        # -------------------------
        # Update global position for free exercise
        # -------------------------
        if exercise_update.position is not None and exercise_update.position != old_pos:
            total_items = (
                self.block_dao.count_by_session(session_id)
                + self.exercise_dao.count_free_by_session(session_id)
                - 1  # l'exercice existe déjà
            )
            if exercise_update.position < 0 or exercise_update.position > total_items:
                raise ValueError("Invalid exercise position")
            items_to_shift = [
                ex for ex in self.exercise_dao.list_by_session(session_id) if ex.position is not None
            ] + self.block_dao.list_by_session(session_id)
            for item in sorted(items_to_shift, key=lambda e: e.position or 0, reverse=old_pos > exercise_update.position):
                pos = item.position or 0
                if old_pos < exercise_update.position and old_pos < pos <= exercise_update.position:
                    item.position = pos - 1
                elif old_pos > exercise_update.position and exercise_update.position <= pos < old_pos:
                    item.position = pos + 1
                if isinstance(item, Exercise):
                    self.exercise_dao.update(item)
                elif isinstance(item, Block):
                    self.block_dao.update(item)
            exercise.position = exercise_update.position

        # -------------------------
        # Update other fields
        # -------------------------
        if exercise_update.exercise_type is not None:
            exercise.exercise_type = exercise_update.exercise_type
        if exercise_update.weight_kg is not None:
            exercise.weight_kg = exercise_update.weight_kg
        if exercise_update.repetitions is not None:
            exercise.repetitions = exercise_update.repetitions
        if exercise_update.duration_seconds is not None:
            exercise.duration_seconds = exercise_update.duration_seconds
        if exercise_update.distance_meters is not None:
            exercise.distance_meters = exercise_update.distance_meters
        if exercise_update.notes is not None:
            exercise.notes = exercise_update.notes

        return self.exercise_dao.update(exercise)

    # -------------------------
    # Delete
    # -------------------------
    def delete_exercise(self, exercise_id: uuid.UUID, user_id:uuid.UUID) -> None:
        """
        Delete an exercise and shift remaining exercises and blocks to fill the gap.
        Handles exercises inside a block and free exercises differently.
        """
        self.ownership_service.check_user_is_owner_exercise(user_id=user_id, exercise_id=exercise_id)
        exercise = self.exercise_dao.get_by_id(exercise_id)
        if not exercise:
            raise ValueError("Exercise not found")

        session_id = exercise.session_id
        block_id = exercise.block_id
        self.exercise_dao.delete(exercise)

        if block_id is not None:
            deleted_pos = exercise.position_in_block or 0
            for ex in sorted(
                (ex for ex in self.exercise_dao.list_by_session(session_id)
                 if ex.id != exercise.id and ex.block_id == block_id),
                key=lambda ex: ex.position_in_block or 0
            ):
                pos = ex.position_in_block or 0
                if pos > deleted_pos:
                    ex.position_in_block = pos - 1
                    self.exercise_dao.update(ex)
        else:
            deleted_pos = exercise.position or 0
            items_to_shift = [
                ex for ex in self.exercise_dao.list_by_session(session_id) if ex.position is not None
            ] + self.block_dao.list_by_session(session_id)
            for item in sorted(items_to_shift, key=lambda item: item.position or 0):
                pos = item.position or 0
                if pos > deleted_pos:
                    item.position = pos - 1
                    if isinstance(item, Exercise):
                        self.exercise_dao.update(item)
                    elif isinstance(item, Block):
                        self.block_dao.update(item)

