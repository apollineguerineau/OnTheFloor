from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session as DBSession

from src.api.deps import get_db
from src.api.schemas.exercise import ExerciseCreate, ExerciseRead, ExerciseUpdate
from src.services.exercise_service import ExerciseService
import uuid

router = APIRouter(prefix="/exercises", tags=["exercises"])


@router.post("/", response_model=ExerciseRead)
def create_exercise(
    payload: ExerciseCreate,
    db: DBSession = Depends(get_db),
):
    try:
        exercise = ExerciseService(db).create_exercise(**payload.model_dump())
        return exercise
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.get("/{exercise_id}", response_model=ExerciseRead)
def get_exercise(exercise_id: uuid.UUID, db: DBSession = Depends(get_db)):
    service = ExerciseService(db)
    exercise = service.get_exercise(exercise_id)
    if not exercise:
        raise HTTPException(status_code=404, detail="Exercise not found")
    return exercise


@router.get("/session/{session_id}", response_model=list[ExerciseRead])
def list_exercises_by_session(session_id: uuid.UUID, db: DBSession = Depends(get_db)):
    service = ExerciseService(db)
    return service.list_by_session(session_id)


@router.get("/block/{block_id}", response_model=list[ExerciseRead])
def list_exercises_by_block(block_id: uuid.UUID, db: DBSession = Depends(get_db)):
    service = ExerciseService(db)
    return service.list_by_block(block_id)

@router.patch("/{exercise_id}", response_model=ExerciseRead)
def update_block(
    exercise_id: uuid.UUID,
    payload: ExerciseUpdate,
    db: DBSession = Depends(get_db),
):
    try:
        return ExerciseService(db).update_exercise(
            exercise_id,
            **payload.model_dump(exclude_unset=True),
        )
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
    
@router.delete("/{exercise_id}", status_code=204)
def delete_exercise(exercise_id: uuid.UUID, db: DBSession = Depends(get_db)):
    try:
        ExerciseService(db).delete_exercise(exercise_id)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))