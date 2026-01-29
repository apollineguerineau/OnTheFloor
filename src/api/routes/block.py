from fastapi import APIRouter, Depends, HTTPException
from src.core.injector import injector
from src.api.deps import authenticate
from src.security.schema import Credentials

from src.api.schemas.block import (
    BlockCreate,
    BlockUpdate,
)
from src.core.entities import BlockEntity
import uuid

router = APIRouter(prefix="/blocks", tags=["blocks"])


@router.post("/")
def create_block(
    block_create: BlockCreate,
    credentials: Credentials = Depends(authenticate)
) -> uuid.UUID:
    try:
        user_id = credentials.user_id
        block_service = injector.block_service()
        return block_service.create_block(block_create, user_id)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))


@router.get("/{block_id}", response_model=BlockEntity)
def get_block(block_id: uuid.UUID, credentials: Credentials = Depends(authenticate) ):
    try:
        user_id = credentials.user_id
        block_service = injector.block_service()
        block = block_service.get_block(block_id, user_id)
        if not block:
            raise HTTPException(status_code=404, detail="Block not found")
        return block
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))


@router.get("/session/{session_id}", response_model=list[BlockEntity])
def list_blocks_by_session(
    session_id: uuid.UUID, credentials: Credentials = Depends(authenticate) 
):
    try:
        user_id = credentials.user_id
        block_service = injector.block_service()
        block_service.list_blocks_by_session(session_id, user_id)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))

@router.patch("/{block_id}")
def update_block(
    block_id: uuid.UUID,
    block_update: BlockUpdate,
    credentials: Credentials = Depends(authenticate)
) -> bool:
    try:
        user_id = credentials.user_id
        block_service = injector.block_service()
        return(block_service.update_block(
            block_id,
            block_update,
            user_id
        ))
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))


@router.delete("/{block_id}", status_code=204)
def delete_block(block_id: uuid.UUID, credentials: Credentials = Depends(authenticate) ) -> bool:
    try:
        user_id = credentials.user_id
        block_service = injector.block_service()
        return(block_service.delete_block(block_id, user_id))
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
