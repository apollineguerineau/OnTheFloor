from sqlalchemy.orm import Session as DBSession

from src.data.dao.block_dao import BlockDAO
from src.data.models import Block, BlockType, Exercise
from src.services.session_service import SessionService
from src.data.dao.exercise_dao import ExerciseDAO


class BlockService:
    def __init__(self, db: DBSession):
        """
        Initialize the BlockService with DAOs for blocks and exercises.
        """
        self.block_dao = BlockDAO(db)
        self.session_service = SessionService(db)
        self.exercise_dao = ExerciseDAO(db)

    # -------------------------
    # List / Get
    # -------------------------
    def get_block(self, block_id: int) -> Block | None:
        """
        Retrieve a block by its ID.
        Returns None if not found.
        """
        return self.block_dao.get_by_id(block_id)

    def list_blocks_by_session(self, session_id: int) -> list[Block]:
        """
        List all blocks for a session, ordered by their position.
        """
        return self.block_dao.list_by_session(session_id)

    # -------------------------
    # Helper: shift positions
    # -------------------------
    def _shift_positions(self, items, removed_pos: int):
        """
        Shift the positions of all items whose position is greater than removed_pos.
        Works for both Block and Exercise objects.
        """
        for item in sorted(items, key=lambda e: e.position or 0):
            if (item.position or 0) > removed_pos:
                item.position = (item.position or 0) - 1
                if isinstance(item, Block):
                    self.block_dao.update(item)
                elif isinstance(item, Exercise):
                    self.exercise_dao.update(item)

    # -------------------------
    # Create
    # -------------------------
    def create_block(
        self,
        *,
        block_type: BlockType,
        session_id: int,
        position: int | None = None,
        duration: float | None = None,
        notes: str | None = None,
    ) -> Block:
        """
        Create a new block in a session.
        If position is not provided, it will be appended at the end.
        Shifts other blocks and free exercises if needed to avoid conflicts.
        """
        session = self.session_service.get_session(session_id)
        if not session:
            raise ValueError("Session not found")

        # Auto-assign position if not provided
        if position is None:
            raise ValueError("Please provide a position for the block.")
        else:
            # Shift existing blocks and free exercises to make room
            items_to_shift = [
                b for b in self.block_dao.list_by_session(session_id)
            ] + [
                e for e in self.exercise_dao.list_by_session(session_id) if e.block_id is None
            ]
            for item in sorted(items_to_shift, key=lambda e: e.position or 0, reverse=True):
                if (item.position or 0) >= position:
                    item.position = (item.position or 0) + 1
                    if isinstance(item, Block):
                        self.block_dao.update(item)
                    else:
                        self.exercise_dao.update(item)

        block = Block(
            block_type=block_type,
            position=position,
            session_id=session_id,
            duration=duration,
            notes=notes,
        )
        return self.block_dao.create(block)

    # -------------------------
    # Update
    # -------------------------
    def update_block(
        self,
        block_id: int,
        *,
        block_type: BlockType | None = None,
        position: int | None = None,
        duration: float | None = None,
        notes: str | None = None,
    ) -> Block:
        """
        Update the properties of a block.
        Adjusts positions of other blocks and free exercises if the position changes.
        """
        block = self.block_dao.get_by_id(block_id)
        if not block:
            raise ValueError("Block not found")

        session_id = block.session_id
        old_position = block.position

        if position is not None and position != old_position:
            items_to_shift = [
                ex for ex in self.exercise_dao.list_by_session(session_id) if ex.position is not None
            ] + self.block_dao.list_by_session(session_id)
            for item in sorted(items_to_shift, key=lambda e: e.position or 0, reverse=old_position > position):
                pos = item.position or 0
                if old_position < position and old_position < pos <= position:
                    item.position = pos - 1
                elif old_position > position and position <= pos < old_position:
                    item.position = pos + 1
                if isinstance(item, Exercise):
                    self.exercise_dao.update(item)
                elif isinstance(item, Block):
                    self.block_dao.update(item)
    
            block.position = position

        if block_type is not None:
            block.block_type = block_type
        if duration is not None:
            block.duration = duration
        if notes is not None:
            block.notes = notes

        return self.block_dao.update(block)

    # -------------------------
    # Delete
    # -------------------------
    def delete_block(self, block_id: int) -> None:
        """
        Delete a block and shift positions of remaining blocks and free exercises.
        """
        block = self.block_dao.get_by_id(block_id)
        if not block:
            raise ValueError("Block not found")

        session_id = block.session_id
        pos_to_remove = block.position

        # Delete the block
        self.block_dao.delete(block)

        # Shift other blocks and free exercises to fill the gap
        items_to_shift = [
            b for b in self.block_dao.list_by_session(session_id)
        ] + [
            e for e in self.exercise_dao.list_by_session(session_id) if e.block_id is None
        ]
        self._shift_positions(items_to_shift, pos_to_remove)


