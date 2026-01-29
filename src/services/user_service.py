from sqlalchemy.orm import Session
from src.data.dao.user_dao import UserDAO
from src.data.models import User
from src.api.schemas.user import UserCreate
import uuid
from src.security.password import hash_password, verify_password

class UserService:
    def __init__(self, db: Session):
        self.dao = UserDAO(db)

    def create_user(self, dto: UserCreate) -> User:
        existing = self.dao.get_by_username(dto.username)
        if existing is not None:
            raise ValueError("User already exists")
        
        hashed_password = hash_password(dto.password)
        return self.dao.create(dto.username, hashed_password)
   
    def get_user(self,user_id: uuid.UUID) -> User | None:
        return self.dao.get_by_id(user_id)
    
    def authenticate(self, username: str, password: str) -> User | None:
        user = self.dao.get_by_username(username)
        if not user:
            return None

        if not verify_password(password, user.hashed_password):
            return None

        return user
    
