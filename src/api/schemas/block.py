from pydantic import BaseModel, Field
from src.data.models import BlockType
import uuid


class BlockCreate(BaseModel):
    block_type: BlockType = Field(..., description="Type of the block")
    position: int| None = Field(None, description="Position of the block within the session")
    session_id: uuid.UUID = Field(..., description="ID of the session this block belongs to")
    duration: float | None = Field(
        None,
        description="Optional duration of the block in minutes",
    )
    notes: str | None = Field(
        None,
        description="Optional notes for the block",
    )

    model_config = {
        "populate_by_name": True,
        "extra": "forbid",
    }


class BlockUpdate(BaseModel):
    block_type: BlockType | None = Field(
        None,
        description="Updated type of the block",
    )
    position: int | None = Field(
        None,
        description="Updated position of the block within the session",
    )
    duration: float | None = Field(
        None,
        description="Updated duration of the block in minutes",
    )
    notes: str | None = Field(
        None,
        description="Updated notes for the block",
    )

    model_config = {
        "populate_by_name": True,
        "extra": "forbid",
    }


class BlockRead(BaseModel):
    id: uuid.UUID
    block_type: BlockType
    position: int
    session_id: uuid.UUID
    duration: float | None
    notes: str | None

    model_config = {
        "populate_by_name": True,
        "from_attributes": True,
        "extra": "forbid",
    }
