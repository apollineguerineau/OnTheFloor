import pytest
from unittest.mock import MagicMock
from datetime import date
from src.data.models import Session, SessionType

def test_create_session(session_service,mock_services_dao):
    mock_dao = mock_services_dao['session']
    location_service = mock_services_dao['session_location']
    mock_session = Session(
        name="Morning WOD",
        date=date(2026, 1, 1),
        session_type=SessionType.wod,
        user_id=1,
        notes="Fun!",
        location_id=1,
    )
    mock_dao.create.return_value = mock_session
    location_service.get_location.return_value = MagicMock(id=1)

    result = session_service.create_session(
        name="Morning WOD",
        date=date(2026, 1, 1),
        session_type=SessionType.wod,
        user_id=1,
        notes="Fun!",
        location_id=1
    )

    location_service.get_location.assert_called_once_with(1)
    mock_dao.create.assert_called_once()
    assert result == mock_session
    assert result.location_id == 1


def test_create_session_invalid_location(session_service, mock_services_dao):
    location_service = mock_services_dao['session_location']
    location_service.get_location.return_value = None

    with pytest.raises(ValueError, match="Location with id 99 not found"):
        session_service.create_session(
            name="WOD",
            date=date(2026, 1, 1),
            session_type=SessionType.wod,
            user_id=1,
            location_id=99
        )


def test_update_session_with_location(session_service,mock_services_dao):
    location_service = mock_services_dao['session_location']
    mock_dao = mock_services_dao['session']
    mock_session = MagicMock()
    mock_dao.get_by_id.return_value = mock_session
    mock_dao.update.return_value = mock_session
    location_service.get_location.return_value = MagicMock(id=2)

    result = session_service.update_session(
        1,
        name="Updated WOD",
        location_id=2
    )

    location_service.get_location.assert_called_once_with(2)
    mock_dao.update.assert_called_once_with(mock_session)
    assert mock_session.name == "Updated WOD"
    assert mock_session.location_id == 2
    assert result == mock_session


def test_update_session_invalid_location(session_service, mock_services_dao):
    location_service = mock_services_dao['session_location']
    mock_dao = mock_services_dao['session']
    mock_session = MagicMock()
    mock_dao.get_by_id.return_value = mock_session
    location_service.get_location.return_value = None

    with pytest.raises(ValueError, match="Location with id 99 not found"):
        session_service.update_session(1, location_id=99)

def test_get_session(session_service, mock_services_dao):
    mock_dao = mock_services_dao['session']
    mock_session = MagicMock()
    mock_dao.get_by_id.return_value = mock_session

    result = session_service.get_session(1)
    mock_dao.get_by_id.assert_called_once_with(1)
    assert result == mock_session


def test_get_sessions_by_date(session_service, mock_services_dao):
    mock_dao = mock_services_dao['session']
    mock_session = MagicMock()
    mock_dao.get_by_date_and_user.return_value = mock_session

    result = session_service.get_sessions_by_date(session_date=date(2026,1,1), user_id=1)
    mock_dao.get_by_date_and_user.assert_called_once_with(session_date=date(2026,1,1), user_id=1)
    assert result == mock_session


def test_list_sessions_by_user(session_service, mock_services_dao):
    mock_dao = mock_services_dao['session']
    mock_list = [MagicMock(), MagicMock()]
    mock_dao.list_by_user.return_value = mock_list

    result = session_service.list_sessions_by_user(user_id=1)
    mock_dao.list_by_user.assert_called_once_with(1)
    assert result == mock_list

def test_get_sessions_by_location_and_user(session_service, mock_services_dao):
    mock_dao = mock_services_dao['session']
    mock_list = [MagicMock(), MagicMock()]
    mock_dao.get_by_location_and_user.return_value = mock_list

    result = session_service.get_sessions_by_location(location_id=1, user_id=2)
    mock_dao.get_by_location_and_user.assert_called_once_with(1, 2)
    assert result == mock_list



def test_update_session_not_found(session_service, mock_services_dao):
    mock_dao = mock_services_dao['session']
    mock_dao.get_by_id.return_value = None

    with pytest.raises(ValueError, match="Session not found"):
        session_service.update_session(99, name="Nope")


def test_delete_session_success(session_service, mock_services_dao):
    mock_dao = mock_services_dao['session']
    mock_session = MagicMock()
    mock_dao.get_by_id.return_value = mock_session

    session_service.delete_session(1)
    mock_dao.get_by_id.assert_called_once_with(1)
    mock_dao.delete.assert_called_once_with(mock_session)


def test_delete_session_not_found(session_service, mock_services_dao):
    mock_dao = mock_services_dao['session']
    mock_dao.get_by_id.return_value = None

    with pytest.raises(ValueError, match="Session not found"):
        session_service.delete_session(99)
