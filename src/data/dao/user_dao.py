from sqlalchemy.orm import Session
from src.data.models import User
import uuid

class UserDAO:
    def __init__(self, db: Session):
        self.db = db

    def get_by_username(self, username: str) -> User | None:
        return (
            self.db.query(User)
            .filter(User.username == username)
            .one_or_none()
        )

    def create(self, username: str) -> User:
        user = User(username=username)
        self.db.add(user)
        self.db.commit()
        self.db.refresh(user)
        return user


    def get_by_id(self,user_id: uuid.UUID) -> User | None:
        return self.db.get(User, user_id)

