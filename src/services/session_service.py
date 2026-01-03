from datetime import date as d
from sqlalchemy.orm import Session as DBSession

from src.data.dao.session_dao import SessionDAO
from src.data.models import Session
from src.data.models import SessionType


class SessionService:
    def __init__(self, db: DBSession):
        self.dao = SessionDAO(db)

    def create_session(
        self,
        *,
        name: str,
        date: d,
        session_type: SessionType,
        user_id: int,
        notes: str | None = None,
    ) -> Session:
        session = Session(
            name=name,
            date=date,
            session_type=session_type,
            user_id=user_id,
            notes=notes,
        )
        return self.dao.create(session)

    def get_session(self, session_id: int) -> Session | None:
        return self.dao.get_by_id(session_id)
    
    def get_session_by_date(
        self,
        *,
        session_date: d,
        user_id: int,
    ) -> Session | None:
        return self.dao.get_by_date_and_user(
            session_date=session_date,
            user_id=user_id,
        )

    def list_sessions_by_user(self, user_id: int) -> list[Session]:
        return self.dao.list_by_user(user_id)

    def update_session(
        self,
        session_id: int,
        *,
        name: str | None = None,
        notes: str | None = None,
        date : d | None = None
    ) -> Session:
        session = self.dao.get_by_id(session_id)
        if not session:
            raise ValueError("Session not found")

        if name is not None:
            session.name = name
        if notes is not None:
            session.notes = notes
        if date is not None:
            session.date = date # type: ignore[assignment]

        return self.dao.update(session)

    def delete_session(self, session_id: int) -> None:
        session = self.dao.get_by_id(session_id)
        if not session:
            raise ValueError("Session not found")

        self.dao.delete(session)

