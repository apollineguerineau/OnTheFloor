from fastapi import APIRouter, Depends, HTTPException, Query
from datetime import date
from src.api.schemas.session import SessionCreate, SessionEntity, SessionUpdate
import uuid
from src.api.deps import authenticate
from src.security.schema import Credentials
from src.core.injector import injector


router = APIRouter(prefix="/sessions", tags=["sessions"])


@router.post("/")
def create_session(
    session_create: SessionCreate,
    credentials: Credentials = Depends(authenticate)
)-> uuid.UUID:
    try:
        session_service = injector.exercise_service()
        user_id = credentials.user_id
        return session_service.create_session(user_id, session_create)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.get("/{session_id}", response_model=SessionEntity)
def get_session(session_id: uuid.UUID, 
                credentials: Credentials = Depends(authenticate)):
    try:
        session_service = injector.exercise_service()
        user_id = credentials.user_id
        session = session_service.get_session(user_id, session_id)
        if not session:
            raise HTTPException(status_code=404, detail="Session not found")
        return session
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.get("/by-date/", response_model=list[SessionEntity])
def get_session_by_date(
    session_date: date = Query(...),
    credentials: Credentials = Depends(authenticate),
):
    try:
        session_service = injector.exercise_service()
        user_id = credentials.user_id
        return session_service.get_sessions_by_date(
            session_date=session_date,
            user_id=user_id,
        )
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.get("/by-location/", response_model=list[SessionEntity])
def get_sessions_by_location(
    location_id: uuid.UUID = Query(...),
    credentials: Credentials = Depends(authenticate),
     
):
    try:
        session_service = injector.exercise_service()
        user_id = credentials.user_id
        return session_service.get_sessions_by_location(location_id=location_id, user_id=user_id)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.get("/user/{user_id}", response_model=list[SessionEntity])
def list_sessions_by_user(
                          credentials: Credentials = Depends(authenticate)):
    
    try:
        session_service = injector.exercise_service()
        user_id = credentials.user_id
        return session_service.list_sessions_by_user(user_id)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.patch("/{session_id}")
def update_session(
    session_id: uuid.UUID,
    session_update: SessionUpdate,
    credentials: Credentials = Depends(authenticate)
) -> bool:
    try:
        session_service = injector.exercise_service()
        user_id = credentials.user_id
        return session_service.update_session(
            session_id, user_id, session_update)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))


@router.delete("/{session_id}", status_code=204)
def delete_session(session_id: uuid.UUID, 
                   credentials: Credentials = Depends(authenticate)) -> bool:
    try:
        session_service = injector.exercise_service()
        user_id = credentials.user_id
        session_service.delete_session(user_id, session_id)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))

