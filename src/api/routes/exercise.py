from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session as DBSession

from src.api.deps import get_db
from src.api.schemas.exercise import ExerciseCreate,ExerciseUpdate
from src.core.entities import ExerciseEntity
import uuid
from src.api.deps import authenticate
from src.security.schema import Credentials

from src.core.injector import injector

router = APIRouter(prefix="/exercises", tags=["exercises"])


@router.post("/")
def create_exercise(
    exercise_create: ExerciseCreate,
    credentials: Credentials = Depends(authenticate)
) -> uuid.UUID:
    
    try:
        exercise_service = injector.exercise_service()
        user_id = credentials.user_id
        exercise_id = exercise_service.create_exercise(exercise_create, user_id)
        return exercise_id
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.get("/{exercise_id}", response_model=ExerciseEntity)
def get_exercise(
    exercise_id: uuid.UUID, 
    credentials: Credentials = Depends(authenticate)
):
    try:
        exercise_service = injector.exercise_service()
        user_id = credentials.user_id
        exercise = exercise_service.get_exercise(exercise_id, user_id)
        if not exercise:
            raise HTTPException(status_code=404, detail="Exercise not found")
        return exercise
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.get("/session/{session_id}", response_model=list[ExerciseEntity])
def list_exercises_by_session(
    session_id: uuid.UUID, 
    credentials: Credentials = Depends(authenticate)
):
    try:
        exercise_service = injector.exercise_service()
        user_id = credentials.user_id
        return exercise_service.list_by_session(session_id, user_id)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.get("/block/{block_id}", response_model=list[ExerciseEntity])
def list_exercises_by_block(
    block_id: uuid.UUID, 
    credentials: Credentials = Depends(authenticate)
):
    try:
        exercise_service = injector.exercise_service()
        user_id = credentials.user_id
        return exercise_service.list_by_block(block_id, user_id)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.patch("/{exercise_id}")
def update_exercise(
    exercise_id: uuid.UUID,
    exercise_update: ExerciseUpdate,
    credentials: Credentials = Depends(authenticate)
)-> bool:
    try:
        exercise_service = injector.exercise_service()
        user_id = credentials.user_id
        return(exercise_service.update_exercise(
            exercise_id,
            exercise_update,
            user_id)
        )
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
    
@router.delete("/{exercise_id}", status_code=204)
def delete_exercise(exercise_id: uuid.UUID, 
                    credentials: Credentials = Depends(authenticate)
) -> bool:
    try:
        exercise_service = injector.exercise_service()
        user_id = credentials.user_id
        return(exercise_service.delete_exercise(exercise_id, user_id))
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))