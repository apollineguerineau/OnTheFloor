from datetime import date as d
from sqlalchemy.orm import Session as DBSession

from src.data.dao.session_dao import SessionDAO
from src.data.models import Session, SessionType
from src.services.location_service import LocationService


class SessionService:
    def __init__(self, db: DBSession):
        self.dao = SessionDAO(db)
        self.location_service = LocationService(db)

    def create_session(
        self,
        *,
        name: str,
        date: d,
        session_type: SessionType,
        user_id: int,
        notes: str | None = None,
        location_id: int | None = None,
    ) -> Session:
        # Validate location using LocationService
        if location_id is not None:
            location = self.location_service.get_location(location_id)
            if location is None:
                raise ValueError(f"Location with id {location_id} not found")

        session = Session(
            name=name,
            date=date,
            session_type=session_type,
            user_id=user_id,
            notes=notes,
            location_id=location_id,
        )
        return self.dao.create(session)

    def get_session(self, session_id: int) -> Session | None:
        return self.dao.get_by_id(session_id)

    def get_sessions_by_date(
        self,
        *,
        session_date: d,
        user_id: int,
    ) -> list[Session]:
        return self.dao.get_by_date_and_user(
            session_date=session_date,
            user_id=user_id,
        )

    def list_sessions_by_user(self, user_id: int) -> list[Session]:
        return self.dao.list_by_user(user_id)
    
    def get_sessions_by_location(self, location_id: int, user_id: int) -> list["Session"]:
        """
        Return all sessions for a specific location and a specific user.
        """
        return self.dao.get_by_location_and_user(location_id, user_id)

    def update_session(
        self,
        session_id: int,
        *,
        session_type : SessionType| None = None,
        name: str | None = None,
        notes: str | None = None,
        date: d | None = None,
        location_id: int | None = None,
    ) -> Session:
        session = self.dao.get_by_id(session_id)
        if not session:
            raise ValueError("Session not found")

        if session_type is not None:
            session.session_type = session_type
        if name is not None:
            session.name = name
        if notes is not None:
            session.notes = notes
        if date is not None:
            session.date = date  # type: ignore[assignment]

        if location_id is not None:
            # Validate location via LocationService
            location = self.location_service.get_location(location_id)
            if location is None:
                raise ValueError(f"Location with id {location_id} not found")
            session.location_id = location_id

        return self.dao.update(session)

    def delete_session(self, session_id: int) -> None:
        session = self.dao.get_by_id(session_id)
        if not session:
            raise ValueError("Session not found")

        self.dao.delete(session)


