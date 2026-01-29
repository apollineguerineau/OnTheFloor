from sqlalchemy import select
from sqlalchemy.engine import Engine
from datetime import date
import uuid

from src.data.models import Session
from src.core.database import new_session
from src.core.entities import SessionEntity



class SessionDAO:
    def __init__(self, engine: Engine):
        self.engine = engine

    def create(self, session_entity: SessionEntity) -> uuid.UUID:
        with new_session(self.engine) as session:
            model = Session(
                user_id=session_entity.user_id,
                location_id=session_entity.location_id,
                name=session_entity.name,
                date=session_entity.date,
                session_type=session_entity.session_type,
                notes=session_entity.notes,
            )
            session.add(model)
            session.commit()
            session.refresh(model)
            return model.id

    def get_by_id(self, session_id: uuid.UUID) -> SessionEntity | None:
        with new_session(self.engine) as session:
            model = session.get(Session, session_id)
            return model.to_entity() if model else None

    def get_by_date_and_user(
        self,
        *,
        session_date: date,
        user_id: uuid.UUID,
    ) -> list[SessionEntity]:
        stmt = select(Session).where(
            Session.date == session_date,
            Session.user_id == user_id,
        )
        with new_session(self.engine) as session:
            models = session.scalars(stmt).all()
            return [m.to_entity() for m in models]

    def list_by_user(self, user_id: uuid.UUID) -> list[SessionEntity]:
        stmt = select(Session).where(Session.user_id == user_id)
        with new_session(self.engine) as session:
            models = session.scalars(stmt).all()
            return [m.to_entity() for m in models]

    def delete(self, session_id: uuid.UUID) -> None:
        with new_session(self.engine) as session:
            model = session.get(Session, session_id)
            if model:
                session.delete(model)
                session.commit()
