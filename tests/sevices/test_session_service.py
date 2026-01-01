# tests/services/test_session_service.py
import pytest
from unittest.mock import MagicMock
from datetime import date

from src.services.session_service import SessionService
from src.data.models import Session, SessionType


@pytest.fixture
def mock_dao(monkeypatch):
    mock = MagicMock()
    monkeypatch.setattr("src.services.session_service.SessionDAO", lambda db: mock)
    return mock

@pytest.fixture
def service(mock_dao):
    # On peut passer n'importe quoi comme db, DAO est mocké
    return SessionService(db=mock_dao)

def test_create_session(service, mock_dao):
    mock_session = Session(
        name="Morning WOD",
        date=date(2026, 1, 1),
        session_type=SessionType.wod,
        user_id=1,
        notes="Fun!"
    )
    mock_dao.create.return_value = mock_session

    result = service.create_session(
        name="Morning WOD",
        date=date(2026,1,1),
        session_type=SessionType.wod,
        user_id=1,
        notes="Fun!"
    )

    mock_dao.create.assert_called_once()
    assert result == mock_session
    assert result.name == "Morning WOD"

def test_get_session(service, mock_dao):
    mock_session = MagicMock()
    mock_dao.get_by_id.return_value = mock_session

    result = service.get_session(1)
    mock_dao.get_by_id.assert_called_once_with(1)
    assert result == mock_session

def test_get_session_by_date(service, mock_dao):
    mock_session = MagicMock()
    mock_dao.get_by_date_and_user.return_value = mock_session

    result = service.get_session_by_date(session_date=date(2026,1,1), user_id=1)
    mock_dao.get_by_date_and_user.assert_called_once_with(session_date=date(2026,1,1), user_id=1)
    assert result == mock_session

def test_list_sessions_by_user(service, mock_dao):
    mock_list = [MagicMock(), MagicMock()]
    mock_dao.list_by_user.return_value = mock_list

    result = service.list_sessions_by_user(user_id=1)
    mock_dao.list_by_user.assert_called_once_with(1)
    assert result == mock_list

def test_update_session_success(service, mock_dao):
    mock_session = MagicMock()
    mock_dao.get_by_id.return_value = mock_session
    mock_dao.update.return_value = mock_session

    result = service.update_session(1, name="Updated WOD", notes="New notes", date=date(2026,1,2))
    mock_dao.get_by_id.assert_called_once_with(1)
    mock_dao.update.assert_called_once_with(mock_session)
    assert mock_session.name == "Updated WOD"
    assert mock_session.notes == "New notes"
    assert mock_session.date == date(2026,1,2)
    assert result == mock_session

def test_update_session_not_found(service, mock_dao):
    mock_dao.get_by_id.return_value = None

    with pytest.raises(ValueError, match="Session not found"):
        service.update_session(99, name="Nope")

def test_delete_session_success(service, mock_dao):
    mock_session = MagicMock()
    mock_dao.get_by_id.return_value = mock_session

    service.delete_session(1)
    mock_dao.get_by_id.assert_called_once_with(1)
    mock_dao.delete.assert_called_once_with(mock_session)

def test_delete_session_not_found(service, mock_dao):
    mock_dao.get_by_id.return_value = None

    with pytest.raises(ValueError, match="Session not found"):
        service.delete_session(99)