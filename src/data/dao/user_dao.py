from sqlalchemy.engine import Engine
import uuid

from src.data.models import User
from src.core.entities import UserEntity

from src.core.database import new_session


class UserDAO:
    def __init__(self, engine: Engine):
        self.engine = engine

    def get_by_username(self, username: str) -> UserEntity | None:
        with new_session(self.engine) as session:
            model = (
                session.query(User)
                .filter(User.username == username)
                .one_or_none()
            )
            return model.to_entity() if model else None

    def create(self, username: str, hashed_password: str) -> uuid.UUID:
        with new_session(self.engine) as session:
            model = User(
                username=username,
                hashed_password=hashed_password,
            )
            session.add(model)
            session.commit()
            session.refresh(model)
            return model.id

    def get_by_id(self, user_id: uuid.UUID) -> UserEntity | None:
        with new_session(self.engine) as session:
            model = session.get(User, user_id)
            return model.to_entity() if model else None
