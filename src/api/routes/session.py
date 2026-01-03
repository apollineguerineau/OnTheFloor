from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session as DBSession

from src.api.deps import get_db
from src.api.schemas.session import (
    SessionCreate,
    SessionRead,
    SessionUpdate,
)
from src.services.session_service import SessionService

from datetime import date
from fastapi import Query

router = APIRouter(prefix="/sessions", tags=["sessions"])


@router.post("/", response_model=SessionRead)
def create_session(
    payload: SessionCreate,
    db: DBSession = Depends(get_db),
):
    return SessionService(db).create_session(**payload.model_dump())


@router.get("/{session_id}", response_model=SessionRead)
def get_session(session_id: int, db: DBSession = Depends(get_db)):
    session = SessionService(db).get_session(session_id)
    if not session:
        raise HTTPException(status_code=404, detail="Session not found")
    return session

@router.get("/by-date/", response_model=SessionRead)
def get_session_by_date(
    session_date: date = Query(...),
    user_id: int = Query(...),
    db: DBSession = Depends(get_db),
):
    session = SessionService(db).get_session_by_date(
        session_date=session_date,
        user_id=user_id,
    )
    if not session:
        raise HTTPException(status_code=404, detail="Session not found")
    return session

@router.get("/user/{user_id}", response_model=list[SessionRead])
def list_sessions_by_user(user_id: int, db: DBSession = Depends(get_db)):
    return SessionService(db).list_sessions_by_user(user_id)


@router.patch("/{session_id}", response_model=SessionRead)
def update_session(
    session_id: int,
    payload: SessionUpdate,
    db: DBSession = Depends(get_db),
):
    try:
        return SessionService(db).update_session(
            session_id, **payload.model_dump(exclude_unset=True)
        )
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))


@router.delete("/{session_id}", status_code=204)
def delete_session(session_id: int, db: DBSession = Depends(get_db)):
    try:
        SessionService(db).delete_session(session_id)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
