from sqlalchemy.orm import Session as DBSession
from sqlalchemy import select, func
import uuid

from src.data.models import Block


class BlockDAO:
    def __init__(self, db: DBSession):
        self.db = db

    def create(self, block: Block) -> Block:
        self.db.add(block)
        self.db.commit()
        self.db.refresh(block)
        return block

    def get_by_id(self, block_id: uuid.UUID) -> Block | None:
        return self.db.get(Block, block_id)

    def list_by_session(self, session_id: uuid.UUID) -> list[Block]:
        stmt = (
                select(Block)
                .where(Block.session_id == session_id)
                .order_by(Block.position)
            )
        return list(self.db.scalars(stmt))

    def update(self, block: Block) -> Block:
        self.db.commit()
        self.db.refresh(block)
        return block

    def delete(self, block: Block) -> None:
        self.db.delete(block)
        self.db.commit()
    
    def count_by_session(self, session_id: uuid.UUID) -> int:
        return self.db.scalars(
            select(func.count())
            .select_from(Block)
            .where(Block.session_id == session_id)
        ).one()
    

