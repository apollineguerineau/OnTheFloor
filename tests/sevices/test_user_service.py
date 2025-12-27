import pytest
from sqlalchemy.orm import Session
from src.data.models import User
from src.services.user_service import UserService
from src.data.dao.user_dao import UserDAO
from src.api.schemas.user import UserCreate

def test_create_user(db_session: Session):
    service = UserService(db_session)

    dto = UserCreate(username="john")
    user = service.create_user(dto)

    # Vérifie que l'utilisateur est créé
    assert user.id is not None
    assert str(user.username) == "john"

    # Vérifie qu'on ne peut pas créer un utilisateur avec le même nom
    dto2 = UserCreate(username="john")
    with pytest.raises(ValueError, match="User already exists"):
        service.create_user(dto2)


def test_get_user(db_session: Session):
    service = UserService(db_session)

    # Crée un utilisateur directement via DAO pour tester la récupération
    dao = UserDAO(db_session)
    user = dao.create("alice")

    retrieved = service.get_user(user.id)
    assert retrieved is not None
    assert retrieved.id == user.id
    assert str(retrieved.username) == "alice"

    # Vérifie que get_user retourne None si l'utilisateur n'existe pas
    assert service.get_user(9999) is None
