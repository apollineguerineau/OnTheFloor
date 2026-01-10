from unittest.mock import MagicMock
from src.data.models import Block, BlockType


def test_create(block_dao, mock_dbs):
    mock_db = mock_dbs["block"]

    block = Block(
        block_type=BlockType.amrap,
        position=1,
        session_id=1,
        duration=12,
        notes="Warm up",
    )

    result = block_dao.create(block)

    mock_db.add.assert_called_once_with(block)
    mock_db.commit.assert_called_once()
    mock_db.refresh.assert_called_once_with(block)
    assert result == block


def test_get_by_id(block_dao, mock_dbs):
    mock_db = mock_dbs["block"]
    mock_db.get.return_value = "found"

    result = block_dao.get_by_id(1)

    mock_db.get.assert_called_once_with(Block, 1)
    assert result == "found"


def test_list_by_session(block_dao, mock_dbs):
    mock_db = mock_dbs["block"]
    mock_db.scalars.return_value = ["b1", "b2"]

    result = block_dao.list_by_session(session_id=1)

    mock_db.scalars.assert_called_once()
    assert result == ["b1", "b2"]


def test_update(block_dao, mock_dbs):
    mock_db = mock_dbs["block"]
    block = MagicMock()

    result = block_dao.update(block)

    mock_db.commit.assert_called_once()
    mock_db.refresh.assert_called_once_with(block)
    assert result == block


def test_delete(block_dao, mock_dbs):
    mock_db = mock_dbs["block"]
    block = MagicMock()

    block_dao.delete(block)

    mock_db.delete.assert_called_once_with(block)
    mock_db.commit.assert_called_once()

def test_count_by_session(block_dao, mock_dbs):
    mock_db = mock_dbs["block"]

    mock_scalars = MagicMock()
    mock_scalars.one.return_value = 2
    mock_db.scalars.return_value = mock_scalars

    result = block_dao.count_by_session(session_id=1)
    assert result == 2
