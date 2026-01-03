import pytest
from fastapi.testclient import TestClient

from src.main import app

from unittest.mock import MagicMock

from src.services.user_service import UserService
from src.services.session_service import SessionService
from src.services.location_service import LocationService
from src.data.dao.session_dao import SessionDAO
from src.data.dao.user_dao import UserDAO
from src.data.dao.location_dao import LocationDAO

@pytest.fixture
def client(monkeypatch):
    """
    Fixture qui mocke tous les services pour toutes les routes.
    """
    mock_service_instances = {}

    # Mock UserService
    user_mock = MagicMock()
    monkeypatch.setattr(
        "src.api.routes.user.UserService",
        lambda db=None: user_mock
    )
    mock_service_instances['user'] = user_mock

    # Mock SessionService
    session_mock = MagicMock()
    monkeypatch.setattr(
        "src.api.routes.session.SessionService",
        lambda db=None: session_mock
    )
    mock_service_instances['session'] = session_mock

    # Mock LocationService
    location_mock = MagicMock()
    monkeypatch.setattr(
        "src.api.routes.location.LocationService",
        lambda db=None: location_mock
    )
    mock_service_instances['location'] = location_mock

    return TestClient(app), mock_service_instances


@pytest.fixture
def mock_services_dao(monkeypatch):
    """Mock all DAOs for all services."""
    mocks = {}

    # UserService
    user_mock = MagicMock()
    monkeypatch.setattr(
        "src.services.user_service.UserDAO",
        lambda db=None: user_mock
    )
    mocks['user'] = user_mock

    # SessionService
    session_mock = MagicMock()
    monkeypatch.setattr(
        "src.services.session_service.SessionDAO",
        lambda db=None: session_mock
    )
    mocks['session'] = session_mock
    
    session_location_mock = MagicMock()
    monkeypatch.setattr(
        "src.services.session_service.LocationService",
        lambda db=None: session_location_mock
    )
    mocks['session_location'] = session_location_mock

    # LocationService
    location_mock = MagicMock()
    monkeypatch.setattr(
        "src.services.location_service.LocationDAO",
        lambda db=None: location_mock
    )
    mocks['location'] = location_mock

    return mocks


@pytest.fixture
def user_service(mock_services_dao):
    """UserService avec DAO mocké."""
    return UserService(db=mock_services_dao['user'])


@pytest.fixture
def session_service(mock_services_dao):
    """SessionService avec DAO mocké."""
    return SessionService(db=mock_services_dao['session'])


@pytest.fixture
def location_service(mock_services_dao):
    """LocationService avec DAO mocké."""
    return LocationService(db=mock_services_dao['location'])

@pytest.fixture
def mock_dbs():
    """
    Retourne un dictionnaire de MagicMocks représentant les sessions DB, users DB et locations DB.
    """
    return {
        "session": MagicMock(),
        "user": MagicMock(),
        "location": MagicMock(),
    }

@pytest.fixture
def session_dao(mock_dbs):
    """SessionDAO avec DB mockée."""
    return SessionDAO(mock_dbs["session"])

@pytest.fixture
def user_dao(mock_dbs):
    """UserDAO avec DB mockée."""
    return UserDAO(mock_dbs["user"])

@pytest.fixture
def location_dao(mock_dbs):
    """LocationDAO avec DB mockée."""
    return LocationDAO(mock_dbs["location"])