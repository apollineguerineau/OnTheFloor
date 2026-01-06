from src.data.models import User
from src.api.schemas.user import UserCreate

def test_create_user_success(user_service, mock_services_dao):
    mock_dao = mock_services_dao['user']
    dto = UserCreate(username="john")

    # Aucun utilisateur existant
    mock_dao.get_by_username.return_value = None
    # Création mockée
    mock_user = User(username=dto.username)
    mock_dao.create.return_value = mock_user

    result = user_service.create_user(dto)

    mock_dao.get_by_username.assert_called_once_with("john")
    mock_dao.create.assert_called_once_with("john")
    assert result == mock_user
    assert result.username == "john"


def test_create_user_already_exists(user_service, mock_services_dao):
    mock_dao = mock_services_dao['user']
    dto = UserCreate(username="john")

    # Utilisateur déjà existant
    mock_dao.get_by_username.return_value = User(username="john")

    import pytest
    with pytest.raises(ValueError, match="User already exists"):
        user_service.create_user(dto)

    mock_dao.get_by_username.assert_called_once_with("john")
    mock_dao.create.assert_not_called()


def test_get_user(user_service, mock_services_dao):
    mock_dao = mock_services_dao['user']
    mock_user = User(username="alice")
    mock_dao.get_by_id.return_value = mock_user

    result = user_service.get_user(user_id=1)

    mock_dao.get_by_id.assert_called_once_with(1)
    assert result == mock_user
    assert result.username == "alice"


def test_get_user_not_found(user_service, mock_services_dao):
    mock_dao = mock_services_dao['user']
    mock_dao.get_by_id.return_value = None

    result = user_service.get_user(user_id=99)

    mock_dao.get_by_id.assert_called_once_with(99)
    assert result is None
