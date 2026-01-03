from unittest.mock import MagicMock
from src.data.models import User

def test_create_user(user_dao,mock_dbs):
    mock_db = mock_dbs['user']
    username = "john"

    # Mock les méthodes SQLAlchemy
    mock_db.add.return_value = None
    mock_db.commit.return_value = None
    mock_db.refresh.return_value = None

    # Appel de la méthode DAO
    result = user_dao.create(username=username)

    mock_db.add.assert_called_once()
    mock_db.commit.assert_called_once()
    mock_db.refresh.assert_called_once()
    assert result.username == username
    assert isinstance(result, User)


def test_get_by_username_found(user_dao,mock_dbs):
    mock_db = mock_dbs['user']
    # Mock de query().filter().one_or_none()
    mock_query = MagicMock()
    mock_query.filter.return_value.one_or_none.return_value = User(username="alice")
    mock_db.query.return_value = mock_query

    result = user_dao.get_by_username("alice")

    mock_db.query.assert_called_once_with(User)
    mock_query.filter.assert_called_once()
    mock_query.filter.return_value.one_or_none.assert_called_once()
    assert result.username == "alice"


def test_get_by_username_not_found(user_dao,mock_dbs):
    mock_db = mock_dbs['user']
    # Mock renvoyant None si utilisateur inexistant
    mock_query = MagicMock()
    mock_query.filter.return_value.one_or_none.return_value = None
    mock_db.query.return_value = mock_query

    result = user_dao.get_by_username("ghost")

    mock_db.query.assert_called_once_with(User)
    mock_query.filter.assert_called_once()
    mock_query.filter.return_value.one_or_none.assert_called_once()
    assert result is None
