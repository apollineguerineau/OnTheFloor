from pydantic import BaseModel, Field
from src.data.models import LocationType

class LocationCreate(BaseModel):
    name: str = Field(..., description="Name of the location")
    address: str | None = Field(None, description="Optional address of the location")
    location_type: LocationType

    model_config = {
        "populate_by_name": True,
        "extra": "forbid",
    }

class LocationRead(BaseModel):
    id: int
    name: str
    address: str | None
    location_type: LocationType

    model_config = {
        "populate_by_name": True,
        "extra": "forbid",
    }
