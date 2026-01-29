from datetime import date as d
from sqlalchemy.orm import Session as DBSession

from src.data.dao.session_dao import SessionDAO
from src.data.models import Session, SessionType
from src.services.location_service import LocationService
from src.api.schemas.session import SessionCreate, SessionUpdate, SessionRead
import uuid

class SessionService:
    def __init__(self, db: DBSession):
        self.dao = SessionDAO(db)
        self.location_service = LocationService(db)

    def create_session(
        self,
        user_id: uuid.UUID,
        session_create : SessionCreate
    ) -> Session:
        # Validate location using LocationService
        if session_create.location_id is not None:
            location = self.location_service.get_location(session_create.location_id)
            if location is None:
                raise ValueError(f"Location with id {session_create.location_id} not found")

        session = Session(
            name=session_create.name,
            date=session_create.date,
            session_type=session_create.session_type,
            user_id=user_id,
            notes=session_create.notes,
            location_id=session_create.location_id,
        )
        return self.dao.create(session)
    
    def check_user_is_owner(self, user_id: uuid.UUID, session_id: uuid.UUID) -> None:
        session = self.dao.get_by_id(session_id)
        if not session:
            raise ValueError("Session not found")
        if session.user_id != user_id:
            raise PermissionError("User does not have access to this session")

    def get_session(self, user_id : uuid.UUID, session_id: uuid.UUID) -> Session | None:
        self.check_user_is_owner(user_id, session_id)
        return self.dao.get_by_id(session_id)

    def get_sessions_by_date(
        self,
        session_date: d,
        user_id: uuid.UUID,
    ) -> list[Session]:
        return self.dao.get_by_date_and_user(
            session_date=session_date,
            user_id=user_id,
        )

    def list_sessions_by_user(self, user_id: uuid.UUID) -> list[Session]:
        return self.dao.list_by_user(user_id)
    
    def get_sessions_by_location(self, location_id: uuid.UUID, user_id: uuid.UUID) -> list["Session"]:
        """
        Return all sessions for a specific location and a specific user.
        """
        return self.dao.get_by_location_and_user(location_id, user_id)

    def update_session(
        self,
        session_id: uuid.UUID,
        user_id : uuid.UUID,
        session_update : SessionUpdate
    ) -> Session:
        self.check_user_is_owner(user_id, session_id)
        session = self.dao.get_by_id(session_id)
        if not session:
            raise ValueError("Session not found")

        if session_update.session_type is not None:
            session.session_type = session_update.session_type
        if session_update.name is not None:
            session.name = session_update.name
        if session_update.notes is not None:
            session.notes = session_update.notes
        if session_update.date is not None:
            session.date = session_update.date  # type: ignore[assignment]

        if session_update.location_id is not None:
            # Validate location via LocationService
            location = self.location_service.get_location(session_update.location_id)
            if location is None:
                raise ValueError(f"Location with id {session_update.location_id} not found")
            session.location_id = session_update.location_id

        return self.dao.update(session)

    def delete_session(self, user_id: uuid.UUID, session_id: uuid.UUID) -> None:
        self.check_user_is_owner(user_id, session_id)
        session = self.dao.get_by_id(session_id)
        if not session:
            raise ValueError("Session not found")

        self.dao.delete(session)


