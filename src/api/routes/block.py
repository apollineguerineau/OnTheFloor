from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session as DBSession

from src.api.deps import get_db
from src.api.schemas.block import (
    BlockCreate,
    BlockRead,
    BlockUpdate,
)
from src.services.block_service import BlockService
import uuid

router = APIRouter(prefix="/blocks", tags=["blocks"])


@router.post("/", response_model=BlockRead)
def create_block(
    payload: BlockCreate,
    db: DBSession = Depends(get_db),
):
    try:
        return BlockService(db).create_block(**payload.model_dump())
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))


@router.get("/{block_id}", response_model=BlockRead)
def get_block(block_id: uuid.UUID, db: DBSession = Depends(get_db)):
    block = BlockService(db).get_block(block_id)
    if not block:
        raise HTTPException(status_code=404, detail="Block not found")
    return block


@router.get("/session/{session_id}", response_model=list[BlockRead])
def list_blocks_by_session(
    session_id: uuid.UUID,
    db: DBSession = Depends(get_db),
):
    return BlockService(db).list_blocks_by_session(session_id)


@router.patch("/{block_id}", response_model=BlockRead)
def update_block(
    block_id: uuid.UUID,
    payload: BlockUpdate,
    db: DBSession = Depends(get_db),
):
    try:
        return BlockService(db).update_block(
            block_id,
            **payload.model_dump(exclude_unset=True),
        )
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))


@router.delete("/{block_id}", status_code=204)
def delete_block(block_id: uuid.UUID, db: DBSession = Depends(get_db)):
    try:
        BlockService(db).delete_block(block_id)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
