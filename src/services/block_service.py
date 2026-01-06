from sqlalchemy.orm import Session as DBSession

from src.data.dao.block_dao import BlockDAO
from src.data.models import Block, BlockType
from src.services.session_service import SessionService


class BlockService:
    def __init__(self, db: DBSession):
        self.block_dao = BlockDAO(db)
        self.session_service = SessionService(db)

    def create_block(
        self,
        *,
        block_type: BlockType,
        position: int,
        session_id: int,
        duration: float | None = None,
        notes: str | None = None,
    ) -> Block:
        session = self.session_service.get_session(session_id)
        if not session:
            raise ValueError("Session not found")

        block = Block(
            block_type=block_type,
            position=position,
            session_id=session_id,
            duration=duration,
            notes=notes,
        )
        return self.block_dao.create(block)

    def get_block(self, block_id: int) -> Block | None:
        return self.block_dao.get_by_id(block_id)

    def list_blocks_by_session(self, session_id: int) -> list[Block]:
        return self.block_dao.list_by_session(session_id)

    def update_block(
        self,
        block_id: int,
        *,
        block_type: BlockType | None = None,
        position: int | None = None,
        duration: float | None = None,
        notes: str | None = None,
    ) -> Block:
        block = self.block_dao.get_by_id(block_id)
        if not block:
            raise ValueError("Block not found")

        if block_type is not None:
            block.block_type = block_type
        if position is not None:
            block.position = position
        if duration is not None:
            block.duration = duration
        if notes is not None:
            block.notes = notes

        return self.block_dao.update(block)

    def delete_block(self, block_id: int) -> None:
        block = self.block_dao.get_by_id(block_id)
        if not block:
            raise ValueError("Block not found")

        self.block_dao.delete(block)
