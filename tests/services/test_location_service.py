from unittest.mock import MagicMock
from src.data.models import Location, LocationType

def test_create_location(location_service,mock_services_dao):
    mock_dao = mock_services_dao['location']
    mock_location = Location(name="Box A", address="123 Street", location_type=LocationType.crossfit)
    mock_dao.create.return_value = mock_location

    result = location_service.create_location(name="Box A", address="123 Street", location_type=LocationType.crossfit)

    mock_dao.create.assert_called_once()
    assert result == mock_location


def test_get_location_found(location_service,mock_services_dao):
    mock_dao = mock_services_dao['location']
    mock_location = MagicMock()
    mock_dao.get_by_id.return_value = mock_location

    result = location_service.get_location(1)
    mock_dao.get_by_id.assert_called_once_with(1)
    assert result == mock_location


def test_get_location_not_found(location_service,mock_services_dao):
    mock_dao = mock_services_dao['location']
    mock_dao.get_by_id.return_value = None

    result = location_service.get_location(999)
    assert result is None


def test_list_locations(location_service,mock_services_dao):
    mock_dao = mock_services_dao['location']
    mock_list = [MagicMock(), MagicMock()]
    mock_dao.list.return_value = mock_list

    result = location_service.list_locations()
    mock_dao.list.assert_called_once()
    assert result == mock_list

def test_delete_location_success(location_service,mock_services_dao):
    mock_dao = mock_services_dao['location']
    mock_location = MagicMock()
    mock_dao.get_by_id.return_value = mock_location

    location_service.delete_location(1)

    mock_dao.get_by_id.assert_called_once_with(1)
    mock_dao.delete.assert_called_once_with(mock_location)


def test_delete_location_not_found(location_service,mock_services_dao):
    mock_dao = mock_services_dao['location']
    mock_dao.get_by_id.return_value = None

    import pytest
    with pytest.raises(ValueError, match="Location not found"):
        location_service.delete_location(99)

