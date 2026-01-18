from sqlalchemy.orm import Session
from src.data.dao.user_dao import UserDAO
from src.data.models import User
from src.api.schemas.user import UserCreate
import uuid

class UserService:
    def __init__(self, db: Session):
        self.dao = UserDAO(db)

    def create_user(self, dto: UserCreate):
        existing = self.dao.get_by_username(dto.username)

        if existing is not None:
            raise ValueError("User already exists")

        return self.dao.create(dto.username)
   
    def get_user(self,user_id: uuid.UUID) -> User | None:
        return self.dao.get_by_id(user_id)
