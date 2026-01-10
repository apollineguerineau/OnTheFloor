from sqlalchemy.orm import Session as DBSession

from src.data.dao.exercise_dao import ExerciseDAO
from src.data.dao.block_dao import BlockDAO
from src.data.models import Exercise, ExerciseType, Block


class ExerciseService:
    def __init__(self, db: DBSession):
        """
        Initialize the ExerciseService with DAOs for exercises and blocks.
        """
        self.dao = ExerciseDAO(db)
        self.block_dao = BlockDAO(db)

    # -------------------------
    # List / Get
    # -------------------------
    def list_by_session(self, session_id: int) -> list[Exercise]:
        """
        List all exercises in a session, ordered by their global position.
        """
        return self.dao.list_by_session(session_id)

    def list_by_block(self, block_id: int) -> list[Exercise]:
        """
        List all exercises in a specific block, ordered by position_in_block.
        """
        return self.dao.list_by_block(block_id)

    def get_exercise(self, exercise_id: int) -> Exercise | None:
        """
        Retrieve a single exercise by ID.
        Returns None if not found.
        """
        return self.dao.get_by_id(exercise_id)

    # -------------------------
    # Create
    # -------------------------
    def create_exercise(
        self,
        *,
        exercise_type: ExerciseType,
        session_id: int,
        block_id: int | None = None,
        position: int | None = None,
        position_in_block: int | None = None,
        weight_kg: float | None = None,
        repetitions: int | None = None,
        duration_seconds: float | None = None,
        distance_meters: float | None = None,
        notes: str | None = None,
    ) -> Exercise:
        """
        Create a new exercise either in a block or as a free exercise in the session.
        Handles automatic position assignment and shifts existing exercises/blocks if needed.
        """
        if session_id is None:
            raise ValueError("Exercise must belong to a session")

        # Validate block ownership
        if block_id is not None and not self.dao.validate_block_session(block_id, session_id):
            raise ValueError("Block does not belong to the same session")

        if block_id is not None and position is not None:
            raise ValueError("Cannot specify global position for an exercise inside a block")

        # -------------------------
        # Handle positions
        # -------------------------
        if block_id is not None:
            total = self.dao.count_by_block(block_id)
            # Auto-assign position_in_block if not provided
            if position_in_block is None:
                position_in_block = total
            else:
                if position_in_block < 0 or position_in_block > total:
                    raise ValueError("Invalid position_in_block")
                # Shift existing exercises in the block to make room
                for ex in sorted(
                    self.dao.list_by_block(block_id),
                    key=lambda e: e.position_in_block or 0,
                    reverse=True
                ):
                    pos = ex.position_in_block or 0
                    if pos >= position_in_block:
                        ex.position_in_block = pos + 1
                        self.dao.update(ex)
        else:
            total_items = (
                        self.block_dao.count_by_session(session_id)
                        + self.dao.count_free_by_session(session_id)
                    )
            # Free exercise in session
            if position is None:
                position = total_items
            else : 
                if position < 0 or position > total_items:
                    raise ValueError("Invalid exercise position")
                items_to_shift = [
                    ex for ex in self.dao.list_by_session(session_id) if ex.position is not None
                ] + self.block_dao.list_by_session(session_id)
                for item in sorted(items_to_shift, key=lambda e: e.position or 0, reverse=True):
                    pos = item.position or 0
                    if pos >= position:
                        item.position = pos + 1
                        if isinstance(item, Exercise):
                            self.dao.update(item)
                        elif isinstance(item, Block):
                            self.block_dao.update(item)

        # Create the exercise
        exercise = Exercise(
            exercise_type=exercise_type,
            session_id=session_id,
            block_id=block_id,
            position_in_block=position_in_block,
            position=position,
            weight_kg=weight_kg,
            repetitions=repetitions,
            duration_seconds=duration_seconds,
            distance_meters=distance_meters,
            notes=notes,
        )
        return self.dao.create(exercise)

    # -------------------------
    # Update
    # -------------------------
    def update_exercise(
        self,
        exercise_id: int,
        *,
        exercise_type: ExerciseType | None = None,
        position: int | None = None,
        position_in_block: int | None = None,
        weight_kg: float | None = None,
        repetitions: int | None = None,
        duration_seconds: float | None = None,
        distance_meters: float | None = None,
        notes: str | None = None,
    ) -> Exercise:
        """
        Update an exercise's properties.
        Position changes within a block or global session are handled properly by shifting others.
        Note: block_id cannot be changed; to move to another block, delete and recreate the exercise.
        """
        exercise = self.dao.get_by_id(exercise_id)
        if not exercise:
            raise ValueError("Exercise not found")

        session_id = exercise.session_id
        block_id = exercise.block_id
        old_pos_in_block = exercise.position_in_block or 0
        old_pos = exercise.position or 0

        if block_id is not None and position is not None:
            raise ValueError("Cannot move an exercise out of its block. Delete and create a new one.")

        # -------------------------
        # Update position_in_block
        # -------------------------
        if position_in_block is not None and position_in_block != old_pos_in_block:
            total = self.dao.count_by_block(block_id or 0) - 1
            if position_in_block < 0 or position_in_block > total:
                raise ValueError("Invalid position_in_block")
            for ex in sorted(
                (ex for ex in self.dao.list_by_session(session_id)
                 if ex.id != exercise.id and ex.block_id == block_id),
                key=lambda e: e.position_in_block or 0,
                reverse=old_pos_in_block > position_in_block
            ):
                pos = ex.position_in_block or 0
                if old_pos_in_block < position_in_block and old_pos_in_block < pos <= position_in_block:
                    ex.position_in_block = pos - 1
                elif old_pos_in_block > position_in_block and position_in_block <= pos < old_pos_in_block:
                    ex.position_in_block = pos + 1
                self.dao.update(ex)
            exercise.position_in_block = position_in_block

        # -------------------------
        # Update global position for free exercise
        # -------------------------
        if position is not None and position != old_pos:
            total_items = (
                self.block_dao.count_by_session(session_id)
                + self.dao.count_free_by_session(session_id)
                - 1  # l'exercice existe déjà
            )
            if position < 0 or position > total_items:
                raise ValueError("Invalid exercise position")
            items_to_shift = [
                ex for ex in self.dao.list_by_session(session_id) if ex.position is not None
            ] + self.block_dao.list_by_session(session_id)
            for item in sorted(items_to_shift, key=lambda e: e.position or 0, reverse=old_pos > position):
                pos = item.position or 0
                if old_pos < position and old_pos < pos <= position:
                    item.position = pos - 1
                elif old_pos > position and position <= pos < old_pos:
                    item.position = pos + 1
                if isinstance(item, Exercise):
                    self.dao.update(item)
                elif isinstance(item, Block):
                    self.block_dao.update(item)
            exercise.position = position

        # -------------------------
        # Update other fields
        # -------------------------
        if exercise_type is not None:
            exercise.exercise_type = exercise_type
        if weight_kg is not None:
            exercise.weight_kg = weight_kg
        if repetitions is not None:
            exercise.repetitions = repetitions
        if duration_seconds is not None:
            exercise.duration_seconds = duration_seconds
        if distance_meters is not None:
            exercise.distance_meters = distance_meters
        if notes is not None:
            exercise.notes = notes

        return self.dao.update(exercise)

    # -------------------------
    # Delete
    # -------------------------
    def delete_exercise(self, exercise_id: int) -> None:
        """
        Delete an exercise and shift remaining exercises and blocks to fill the gap.
        Handles exercises inside a block and free exercises differently.
        """
        exercise = self.dao.get_by_id(exercise_id)
        if not exercise:
            raise ValueError("Exercise not found")

        session_id = exercise.session_id
        block_id = exercise.block_id
        self.dao.delete(exercise)

        if block_id is not None:
            deleted_pos = exercise.position_in_block or 0
            for ex in sorted(
                (ex for ex in self.dao.list_by_session(session_id)
                 if ex.id != exercise.id and ex.block_id == block_id),
                key=lambda ex: ex.position_in_block or 0
            ):
                pos = ex.position_in_block or 0
                if pos > deleted_pos:
                    ex.position_in_block = pos - 1
                    self.dao.update(ex)
        else:
            deleted_pos = exercise.position or 0
            items_to_shift = [
                ex for ex in self.dao.list_by_session(session_id) if ex.position is not None
            ] + self.block_dao.list_by_session(session_id)
            for item in sorted(items_to_shift, key=lambda item: item.position or 0):
                pos = item.position or 0
                if pos > deleted_pos:
                    item.position = pos - 1
                    if isinstance(item, Exercise):
                        self.dao.update(item)
                    elif isinstance(item, Block):
                        self.block_dao.update(item)

