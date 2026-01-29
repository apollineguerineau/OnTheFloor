from fastapi import APIRouter, Depends, HTTPException
from src.api.schemas.location import LocationCreate
from src.core.entities import LocationEntity
from src.services.location_service import LocationService
import uuid
from src.api.deps import authenticate
from src.security.schema import Credentials
from src.core.injector import injector


router = APIRouter(prefix="/locations", tags=["locations"])


@router.post("/")
def create_location(location_create: LocationCreate, credentials: Credentials = Depends(authenticate)) -> uuid.UUID:
    try:
        location_service = injector.location_service()
        return location_service.create_location(location_create)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.get("/{location_id}", response_model=LocationEntity)
def get_location(location_id: uuid.UUID,credentials: Credentials = Depends(authenticate)  ):
    try:
        location_service = injector.location_service()
        location = location_service.get_location(location_id)
        if not location:
            raise HTTPException(status_code=404, detail="Location not found")
        return location
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.get("/", response_model=list[LocationEntity])
def list_locations(credentials: Credentials = Depends(authenticate)):
    try:
        location_service = injector.location_service()
        return location_service.list_locations()
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.delete("/{location_id}", status_code=204)
def delete_location(location_id: uuid.UUID, credentials: Credentials = Depends(authenticate) )-> bool:
    try:
        location_service = injector.location_service()
        location_service.delete_location(location_id)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
