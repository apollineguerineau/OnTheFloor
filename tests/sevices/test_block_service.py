import pytest
from unittest.mock import MagicMock
from src.data.models import Block, BlockType


def test_create_block(block_service, mock_services_dao):
    mock_dao = mock_services_dao["block"]
    session_service = mock_services_dao["block_session"]

    mock_block = Block(
        block_type=BlockType.amrap,
        position=1,
        session_id=1,
        duration=12,
        notes="Warm up",
    )

    mock_dao.create.return_value = mock_block
    session_service.get_session.return_value = MagicMock(id=1)

    result = block_service.create_block(
        block_type=BlockType.amrap,
        position=1,
        session_id=1,
        duration=12,
        notes="Warm up",
    )

    session_service.get_session.assert_called_once_with(1)
    mock_dao.create.assert_called_once()
    assert result == mock_block
    assert result.session_id == 1


def test_create_block_invalid_session(block_service, mock_services_dao):
    session_service = mock_services_dao["block_session"]
    session_service.get_session.return_value = None

    with pytest.raises(ValueError, match="Session not found"):
        block_service.create_block(
            block_type=BlockType.emom,
            position=1,
            session_id=99,
        )


def test_update_block(block_service, mock_services_dao):
    mock_dao = mock_services_dao["block"]
    mock_block = MagicMock()

    mock_dao.get_by_id.return_value = mock_block
    mock_dao.update.return_value = mock_block

    result = block_service.update_block(
        1,
        block_type=BlockType.for_time,
        duration=10,
        notes="Updated notes",
    )

    mock_dao.update.assert_called_once_with(mock_block)
    assert mock_block.block_type == BlockType.for_time
    assert mock_block.duration == 10
    assert mock_block.notes == "Updated notes"
    assert result == mock_block


def test_update_block_not_found(block_service, mock_services_dao):
    mock_dao = mock_services_dao["block"]
    mock_dao.get_by_id.return_value = None

    with pytest.raises(ValueError, match="Block not found"):
        block_service.update_block(99, notes="Nope")


def test_get_block(block_service, mock_services_dao):
    mock_dao = mock_services_dao["block"]
    mock_block = MagicMock()
    mock_dao.get_by_id.return_value = mock_block

    result = block_service.get_block(1)

    mock_dao.get_by_id.assert_called_once_with(1)
    assert result == mock_block


def test_list_blocks_by_session(block_service, mock_services_dao):
    mock_dao = mock_services_dao["block"]
    mock_list = [MagicMock(), MagicMock()]
    mock_dao.list_by_session.return_value = mock_list

    result = block_service.list_blocks_by_session(session_id=1)

    mock_dao.list_by_session.assert_called_once_with(1)
    assert result == mock_list


def test_delete_block_success(block_service, mock_services_dao):
    mock_dao = mock_services_dao["block"]
    mock_block = MagicMock()
    mock_dao.get_by_id.return_value = mock_block

    block_service.delete_block(1)

    mock_dao.get_by_id.assert_called_once_with(1)
    mock_dao.delete.assert_called_once_with(mock_block)


def test_delete_block_not_found(block_service, mock_services_dao):
    mock_dao = mock_services_dao["block"]
    mock_dao.get_by_id.return_value = None

    with pytest.raises(ValueError, match="Block not found"):
        block_service.delete_block(99)
