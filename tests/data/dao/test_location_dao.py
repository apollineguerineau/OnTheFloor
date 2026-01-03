from unittest.mock import MagicMock
from src.data.models import Location, LocationType

def test_create(location_dao,mock_dbs):
    mock_db = mock_dbs['location']
    location = Location(name="Box A", address="123 Street", location_type=LocationType.crossfit)
    result = location_dao.create(location)
    mock_db.add.assert_called_once_with(location)
    mock_db.commit.assert_called_once()
    mock_db.refresh.assert_called_once_with(location)
    assert result == location


def test_get_by_id(location_dao,mock_dbs):
    mock_db = mock_dbs['location']
    mock_filter = MagicMock()
    mock_filter.first.return_value = "found"

    mock_db.query.return_value.filter.return_value = mock_filter
    result = location_dao.get_by_id(1)
    assert result == "found"


def test_list_all(location_dao,mock_dbs):
    mock_db = mock_dbs['location']
    mock_db.query.return_value.all.return_value = ["loc1", "loc2"]
    result = location_dao.list()
    assert result == ["loc1", "loc2"]

def test_delete(location_dao,mock_dbs):
    mock_db = mock_dbs['location']
    location = MagicMock()
    location_dao.delete(location)
    mock_db.delete.assert_called_once_with(location)
    mock_db.commit.assert_called_once()

