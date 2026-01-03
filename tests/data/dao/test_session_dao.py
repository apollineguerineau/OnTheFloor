from unittest.mock import MagicMock
from datetime import date
from src.data.models import Session, SessionType

def test_create(session_dao,mock_dbs):
    mock_db = mock_dbs['session']
    session = Session(
        name="Morning WOD",
        date=date(2026, 1, 1),
        session_type=SessionType.wod,
        user_id=1,
        notes="Fun!",
        location_id=None,  # Optional location
    )
    result = session_dao.create(session)
    mock_db.add.assert_called_once_with(session)
    mock_db.commit.assert_called_once()
    mock_db.refresh.assert_called_once_with(session)
    assert result == session

def test_get_by_id(session_dao,mock_dbs):
    mock_db = mock_dbs['session']
    mock_db.get.return_value = "found"
    result = session_dao.get_by_id(1)
    mock_db.get.assert_called_once_with(Session, 1)
    assert result == "found"

def test_get_by_date_and_user(session_dao,mock_dbs):
    mock_db = mock_dbs['session']
    mock_db.scalars.return_value.all.return_value = ["found"]
    
    result = session_dao.get_by_date_and_user(session_date=date(2026, 1, 1), user_id=1)
    
    assert mock_db.scalars.return_value.all.called
    assert result == ["found"]

def test_list_by_user(session_dao,mock_dbs):
    mock_db = mock_dbs['session']
    mock_db.scalars.return_value = ["s1", "s2"]
    result = session_dao.list_by_user(user_id=1)
    mock_db.scalars.assert_called_once()
    assert result == ["s1", "s2"]

def test_get_by_location_and_user(session_dao,mock_dbs):
    mock_db = mock_dbs['session']
    mock_scalars = MagicMock()
    mock_scalars.all.return_value = ["s1", "s2"]
    mock_db.scalars.return_value = mock_scalars

    result = session_dao.get_by_location_and_user(location_id=1, user_id=2)

    mock_db.scalars.assert_called_once()
    assert result == ["s1", "s2"]

def test_update(session_dao,mock_dbs):
    mock_db = mock_dbs['session']
    session = MagicMock()
    mock_db.commit.return_value = None
    mock_db.refresh.return_value = None
    result = session_dao.update(session)
    mock_db.commit.assert_called_once()
    mock_db.refresh.assert_called_once_with(session)
    assert result == session

def test_delete(session_dao,mock_dbs):
    mock_db = mock_dbs['session']
    session = MagicMock()
    session_dao.delete(session)
    mock_db.delete.assert_called_once_with(session)
    mock_db.commit.assert_called_once()

