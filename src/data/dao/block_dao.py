from sqlalchemy.orm import Session as DBSession
from sqlalchemy import select, func
import uuid

from src.data.models import Block
from sqlalchemy import Engine
from src.core.database import new_session
from src.core.entities import BlockEntity
class BlockDAO:
    def __init__(self, engine : Engine):
        self.engine = engine

    def create(self, block_entity: BlockEntity) -> uuid.UUID:
        with new_session(self.engine) as session : 
            block_model = Block(session_id=block_entity.session_id, block_type = block_entity.block_type, duration = block_entity.duration, position = block_entity.position, notes = block_entity.notes)
            session.add(block_model)
            session.commit(block_model)
            session.refresh(block_model)
        return block_model.id

    def get_by_id(self, block_id: uuid.UUID) -> BlockEntity | None:
        with new_session(self.engine) as session :
            block_model = session.get(Block, block_id)
            return block_model.to_entity()

    def list_by_session(self, session_id: uuid.UUID) -> list[Block]:
        stmt = (
                select(Block)
                .where(Block.session_id == session_id)
                .order_by(Block.position)
            )
        with new_session(self.engine) as session :
            blocks_models = list( session.scalars(stmt))
            return [block_model.to_entity() for block_model in blocks_models]

    def update(self, block_entity: BlockEntity) -> None:
        with new_session(self.engine) as session :
            block_model = Block(session_id=block_entity.session_id, block_type = block_entity.block_type, duration = block_entity.duration, position = block_entity.position, notes = block_entity.notes)
            session.commit()
            session.refresh(block_model)

    def delete(self, block_entity: BlockEntity) -> None:
        block_model = Block(session_id=block_entity.session_id, block_type = block_entity.block_type, duration = block_entity.duration, position = block_entity.position, notes = block_entity.notes)
        with new_session(self.engine) as session :
            session.commit()
    
    def count_by_session(self, session_id: uuid.UUID) -> int:
        with new_session(self.engine) as session :
            return  session.scalars(
                select(func.count())
                .select_from(Block)
                .where(Block.session_id == session_id)
            ).one()
    

