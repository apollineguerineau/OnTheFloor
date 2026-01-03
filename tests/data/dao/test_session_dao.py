# tests/data/test_session_dao.py
import pytest
from unittest.mock import MagicMock
from datetime import date

from src.data.dao.session_dao import SessionDAO
from src.data.models import Session, SessionType

@pytest.fixture
def mock_db():
    return MagicMock()

@pytest.fixture
def dao(mock_db):
    return SessionDAO(mock_db)

def test_create(dao, mock_db):
    session = Session(
        name="Morning WOD",
        date=date(2026,1,1),
        session_type=SessionType.wod,
        user_id=1,
        notes="Fun!"
    )
    result = dao.create(session)
    mock_db.add.assert_called_once_with(session)
    mock_db.commit.assert_called_once()
    mock_db.refresh.assert_called_once_with(session)
    assert result == session

def test_get_by_id(dao, mock_db):
    mock_db.get.return_value = "found"
    result = dao.get_by_id(1)
    mock_db.get.assert_called_once_with(Session, 1)
    assert result == "found"

def test_get_by_date_and_user(dao, mock_db):
    mock_db.scalars.return_value.one_or_none.return_value = "found"
    
    # On patch la méthode select pour que scalars soit appelée correctement
    result = dao.get_by_date_and_user(session_date=date(2026,1,1), user_id=1)
    
    # Vérification que scalars et one_or_none ont été appelés
    assert mock_db.scalars.return_value.one_or_none.called
    assert result == "found"

def test_list_by_user(dao, mock_db):
    mock_db.scalars.return_value = ["s1", "s2"]
    result = dao.list_by_user(user_id=1)
    mock_db.scalars.assert_called_once()
    assert result == ["s1", "s2"]

def test_update(dao, mock_db):
    session = MagicMock()
    mock_db.commit.return_value = None
    mock_db.refresh.return_value = None
    result = dao.update(session)
    mock_db.commit.assert_called_once()
    mock_db.refresh.assert_called_once_with(session)
    assert result == session

def test_delete(dao, mock_db):
    session = MagicMock()
    dao.delete(session)
    mock_db.delete.assert_called_once_with(session)
    mock_db.commit.assert_called_once()

