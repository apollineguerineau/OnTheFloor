from sqlalchemy.orm import Session as DBSession
from sqlalchemy import select
from datetime import date

from src.data.models import Session


class SessionDAO:
    def __init__(self, db: DBSession):
        self.db = db

    def create(self, session: Session) -> Session:
        self.db.add(session)
        self.db.commit()
        self.db.refresh(session)
        return session

    def get_by_id(self, session_id: int) -> Session | None:
        return self.db.get(Session, session_id)
    
    def get_by_date_and_user(
        self,
        *,
        session_date: date,
        user_id: int,
    ) -> list["Session"]:
        stmt = (
            select(Session)
            .where(Session.date == session_date)
            .where(Session.user_id == user_id)
        )
        return list(self.db.scalars(stmt).all())

    def list_by_user(self, user_id: int) -> list[Session]:
        stmt = select(Session).where(Session.user_id == user_id)
        return list(self.db.scalars(stmt))

    def get_by_location_and_user(self, location_id: int, user_id: int) -> list["Session"]:
        """
        Return all sessions for a given location and user.
        """
        stmt = select(Session).where(
            (Session.location_id == location_id) &
            (Session.user_id == user_id)
        )
        return list(self.db.scalars(stmt).all())

    def update(self, session: Session) -> Session:
        self.db.commit()
        self.db.refresh(session)
        return session

    def delete(self, session: Session) -> None:
        self.db.delete(session)
        self.db.commit()

