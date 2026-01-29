from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session as DBSession
from datetime import date

from src.api.deps import get_db
from src.api.schemas.session import SessionCreate, SessionRead, SessionUpdate
from src.services.session_service import SessionService
import uuid
from src.api.deps import authenticate
from src.security.schema import Credentials

router = APIRouter(prefix="/sessions", tags=["sessions"])


@router.post("/", response_model=SessionRead)
def create_session(
    session_create: SessionCreate,
    db: DBSession = Depends(get_db),
    credentials: Credentials = Depends(authenticate)
):
    user_id = credentials.user_id
    try:
        return SessionService(db).create_session(user_id, session_create)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.get("/{session_id}", response_model=SessionRead)
def get_session(session_id: uuid.UUID, 
                db: DBSession = Depends(get_db),
                credentials: Credentials = Depends(authenticate)):
    user_id = credentials.user_id
    session = SessionService(db).get_session(user_id, session_id)
    if not session:
        raise HTTPException(status_code=404, detail="Session not found")
    return session


@router.get("/by-date/", response_model=list[SessionRead])
def get_session_by_date(
    session_date: date = Query(...),
    credentials: Credentials = Depends(authenticate),
    db: DBSession = Depends(get_db),
):
    user_id = credentials.user_id
    service = SessionService(db)
    return service.get_sessions_by_date(
        session_date=session_date,
        user_id=user_id,
    )

@router.get("/by-location/", response_model=list[SessionRead])
def get_sessions_by_location(
    location_id: uuid.UUID = Query(...),
    credentials: Credentials = Depends(authenticate),
    db: DBSession = Depends(get_db)
):
    user_id = credentials.user_id
    service = SessionService(db)
    return service.get_sessions_by_location(location_id=location_id, user_id=user_id)


@router.get("/user/{user_id}", response_model=list[SessionRead])
def list_sessions_by_user(db: DBSession = Depends(get_db),
                          credentials: Credentials = Depends(authenticate)):
    user_id = credentials.user_id
    return SessionService(db).list_sessions_by_user(user_id)


@router.patch("/{session_id}", response_model=SessionRead)
def update_session(
    session_id: uuid.UUID,
    session_update: SessionUpdate,
    db: DBSession = Depends(get_db),
    credentials: Credentials = Depends(authenticate)
):
    user_id = credentials.user_id
    try:
        return SessionService(db).update_session(
            session_id, user_id, session_update)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))


@router.delete("/{session_id}", status_code=204)
def delete_session(session_id: uuid.UUID, 
                   db: DBSession = Depends(get_db),
                   credentials: Credentials = Depends(authenticate)):
    user_id = credentials.user_id
    try:
        SessionService(db).delete_session(user_id, session_id)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))

