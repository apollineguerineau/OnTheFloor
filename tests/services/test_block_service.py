import pytest
from unittest.mock import MagicMock
from src.data.models import BlockType


# -------------------------
# Create
# -------------------------

def test_create_block_with_position(block_service, mock_services_dao):
    block_dao = mock_services_dao["block"]
    exercise_dao = mock_services_dao["block_exercise"]
    session_service = mock_services_dao["block_session"]

    session_service.get_session.return_value = MagicMock(id=1)

    existing_block = MagicMock(id=1, position=0)
    free_exercise = MagicMock(id=2, position=1, block_id=None)

    block_dao.list_by_session.return_value = [existing_block]
    exercise_dao.list_by_session.return_value = [free_exercise]

    # ⬇️ AJOUTS
    block_dao.count_by_session.return_value = 1
    exercise_dao.count_free_by_session.return_value = 1

    block_dao.update.side_effect = lambda b: b
    exercise_dao.update.side_effect = lambda e: e
    block_dao.create.side_effect = lambda b: b

    result = block_service.create_block(
        block_type=BlockType.amrap,
        session_id=1,
        position=1,
    )

    assert free_exercise.position == 2
    exercise_dao.update.assert_called_once_with(free_exercise)

    assert result.position == 1
    assert result.session_id == 1
    assert result.block_type == BlockType.amrap


def test_create_block_invalid_session(block_service, mock_services_dao):
    session_service = mock_services_dao["block_session"]
    session_service.get_session.return_value = None

    with pytest.raises(ValueError, match="Session not found"):
        block_service.create_block(
            block_type=BlockType.emom,
            session_id=99,
        )


# -------------------------
# Update
# -------------------------

def test_update_block_position_with_shifts(block_service, mock_services_dao):
    block_dao = mock_services_dao["block"]
    exercise_dao = mock_services_dao["block_exercise"]

    block = MagicMock(id=1, session_id=1, position=0)
    block_dao.get_by_id.return_value = block
    block_dao.update.side_effect = lambda b: b

    other_block = MagicMock(id=2, position=1)
    free_exercise = MagicMock(id=3, position=2, block_id=None)

    block_dao.list_by_session.return_value = [block, other_block]
    exercise_dao.list_by_session.return_value = [free_exercise]

    # ⬇️ AJOUTS
    block_dao.count_by_session.return_value = 2
    exercise_dao.count_free_by_session.return_value = 1

    exercise_dao.update.side_effect = lambda e: e

    result = block_service.update_block(
        block_id=1,
        position=1,
    )

    assert block.position == 1
    assert other_block.position == 0
    assert free_exercise.position == 2

    assert result == block

def test_update_block_not_found(block_service, mock_services_dao):
    block_dao = mock_services_dao["block"]
    block_dao.get_by_id.return_value = None

    with pytest.raises(ValueError, match="Block not found"):
        block_service.update_block(99, notes="Nope")


# -------------------------
# Get / List
# -------------------------

def test_get_block(block_service, mock_services_dao):
    block_dao = mock_services_dao["block"]
    mock_block = MagicMock()
    block_dao.get_by_id.return_value = mock_block

    result = block_service.get_block(1)

    block_dao.get_by_id.assert_called_once_with(1)
    assert result == mock_block


def test_list_blocks_by_session(block_service, mock_services_dao):
    block_dao = mock_services_dao["block"]
    mock_list = [MagicMock(), MagicMock()]
    block_dao.list_by_session.return_value = mock_list

    result = block_service.list_blocks_by_session(1)

    block_dao.list_by_session.assert_called_once_with(1)
    assert result == mock_list


# -------------------------
# Delete
# -------------------------

def test_delete_block_with_shifts(block_service, mock_services_dao):
    block_dao = mock_services_dao["block"]
    exercise_dao = mock_services_dao["block_exercise"]

    block = MagicMock(id=1, session_id=1, position=1)
    block_dao.get_by_id.return_value = block

    remaining_block = MagicMock(position=2)
    free_exercise = MagicMock(position=3, block_id=None)

    block_dao.list_by_session.return_value = [remaining_block]
    exercise_dao.list_by_session.return_value = [free_exercise]

    block_service.delete_block(1)
    assert remaining_block.position == 1
    assert free_exercise.position == 2



def test_delete_block_not_found(block_service, mock_services_dao):
    block_dao = mock_services_dao["block"]
    block_dao.get_by_id.return_value = None

    with pytest.raises(ValueError, match="Block not found"):
        block_service.delete_block(99)

