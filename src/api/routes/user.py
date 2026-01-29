from fastapi import APIRouter, Depends, HTTPException
from src.api.schemas.user import UserCreate
from src.core.entities import UserEntity
import uuid
from src.core.injector import injector
from src.api.deps import authenticate
from src.security.schema import Credentials

router = APIRouter(prefix="/users", tags=["users"])

@router.post("/")
def create_user(
    user_create: UserCreate,
    credentials: Credentials = Depends(authenticate)
)-> uuid.UUID:
    try:
        user_service = injector.user_service()
        return user_service.create_user(user_create)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.get("/{user_id}", response_model=UserEntity)
def get_user(user_id: uuid.UUID,credentials: Credentials = Depends(authenticate)):
    try:
        user_service = injector.user_service()
        user = user_service.get_user(user_id)
        if not user:
            raise HTTPException(status_code=404, detail="User not found")
        return user
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
