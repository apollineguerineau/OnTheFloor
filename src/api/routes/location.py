from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session as DBSession

from src.api.deps import get_db
from src.api.schemas.location import LocationCreate, LocationRead
from src.services.location_service import LocationService
import uuid

router = APIRouter(prefix="/locations", tags=["locations"])


@router.post("/", response_model=LocationRead)
def create_location(payload: LocationCreate, db: DBSession = Depends(get_db)):
    try:
        return LocationService(db).create_location(**payload.model_dump())
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.get("/{location_id}", response_model=LocationRead)
def get_location(location_id: uuid.UUID, db: DBSession = Depends(get_db)):
    location = LocationService(db).get_location(location_id)
    if not location:
        raise HTTPException(status_code=404, detail="Location not found")
    return location


@router.get("/", response_model=list[LocationRead])
def list_locations(db: DBSession = Depends(get_db)):
    return LocationService(db).list_locations()

@router.delete("/{location_id}", status_code=204)
def delete_location(location_id: uuid.UUID, db: DBSession = Depends(get_db)):
    service = LocationService(db)
    try:
        service.delete_location(location_id)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
