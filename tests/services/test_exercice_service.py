from unittest.mock import MagicMock
from src.data.models import Exercise, ExerciseType

# -------------------------
# CREATE
# -------------------------
def test_create_exercise_free(exercise_service, mock_services_dao):
    mock_dao = mock_services_dao['exercise']
    mock_block_dao = mock_services_dao['exercise_block']

    # ⬇️ important
    mock_block_dao.count_by_session.return_value = 0
    mock_dao.count_free_by_session.return_value = 0

    result_exercise = Exercise(
        id=1,
        session_id=1,
        block_id=None,
        position=0,
        position_in_block=None,
        exercise_type=ExerciseType.air_squat,
    )

    mock_dao.create.return_value = result_exercise

    result = exercise_service.create_exercise(
        exercise_type=ExerciseType.air_squat,
        session_id=1,
        position=0,
    )

    mock_dao.create.assert_called_once()
    assert result == result_exercise


def test_create_exercise_in_block(exercise_service, mock_services_dao):
    mock_dao = mock_services_dao['exercise']

    block_id = 1
    result_exercise = Exercise(
        id=2,
        session_id=1,
        block_id=block_id,
        position_in_block=0,
        exercise_type=ExerciseType.air_squat,
    )

    mock_dao.create.return_value = result_exercise
    mock_dao.list_by_block.return_value = []

    result = exercise_service.create_exercise(
        exercise_type=ExerciseType.air_squat,
        session_id=1,
        block_id=block_id
    )

    mock_dao.create.assert_called_once()
    assert result.block_id == block_id
    assert result.position_in_block == 0

# -------------------------
# UPDATE
# -------------------------
def test_update_exercise_free_position(exercise_service, mock_services_dao):
    mock_dao = mock_services_dao['exercise']
    mock_block_dao = mock_services_dao['exercise_block']

    exercise = MagicMock(
        id=1, session_id=1, block_id=None, position=0, position_in_block=None
    )
    mock_dao.get_by_id.return_value = exercise

    other_ex = MagicMock(id=2, block_id=None, position=1)
    block = MagicMock(id=3, position=2)

    mock_dao.list_by_session.return_value = [exercise, other_ex]
    mock_block_dao.list_by_session.return_value = [block]

    # ⬇️ important
    mock_block_dao.count_by_session.return_value = 1
    mock_dao.count_free_by_session.return_value = 2

    mock_dao.update.side_effect = lambda ex: ex
    mock_block_dao.update.side_effect = lambda b: b

    result = exercise_service.update_exercise(
        exercise_id=1,
        position=2
    )

    assert exercise.position == 2
    assert result == exercise



def test_update_exercise_in_block_position(exercise_service, mock_services_dao):
    mock_dao = mock_services_dao['exercise']

    block_id = 1
    exercise = MagicMock(
        id=1, session_id=1, block_id=block_id, position_in_block=0, position=None
    )
    ex_in_block = MagicMock(id=2, block_id=block_id, position_in_block=1)

    mock_dao.get_by_id.return_value = exercise
    mock_dao.list_by_block.return_value = [exercise, ex_in_block]

    # ⬇️ important
    mock_dao.count_by_block.return_value = 2

    mock_dao.update.side_effect = lambda ex: ex

    result = exercise_service.update_exercise(
        exercise_id=1,
        position_in_block=1
    )

    assert exercise.position_in_block == 1
    assert result.id == 1


# -------------------------
# DELETE
# -------------------------
def test_delete_exercise_free(exercise_service, mock_services_dao):
    """
    Delete a free exercise and shift other free exercises and blocks
    """
    mock_dao = mock_services_dao['exercise']
    mock_block_dao = mock_services_dao['exercise_block']

    exercise = MagicMock(id=1, session_id=1, block_id=None, position=1)
    mock_dao.get_by_id.return_value = exercise
    # Other free exercise and block
    other_ex = MagicMock(id=2, block_id=None, position=2)
    block = MagicMock(id=3, position=3)
    mock_dao.list_by_session.return_value = [exercise, other_ex]
    mock_block_dao.list_by_session.return_value = [block]

    exercise_service.delete_exercise(exercise_id=1)
    mock_dao.delete.assert_called_once_with(exercise)
    # Check that other_ex.position is decremented
    assert other_ex.position == 1

def test_delete_exercise_in_block(exercise_service, mock_services_dao):
    """
    Delete an exercise in a block and shift only the other exercises in the same block
    """
    mock_dao = mock_services_dao['exercise']

    block_id = 1
    exercise = MagicMock(id=1, session_id=1, block_id=block_id, position_in_block=0)
    ex_in_block = MagicMock(id=2, session_id=1, block_id=block_id, position_in_block=1)
    ex_other_block = MagicMock(id=3, session_id=1, block_id=2, position_in_block=0)
    ex_free = MagicMock(id=4, session_id=1, block_id=None, position=0)

    mock_dao.get_by_id.return_value = exercise
    mock_dao.list_by_session.return_value = [exercise, ex_in_block, ex_other_block, ex_free]

    exercise_service.delete_exercise(exercise_id=1)
    mock_dao.delete.assert_called_once_with(exercise)
    # Only ex_in_block should be decremented
    assert ex_in_block.position_in_block == 0
    # Free exercises or exercises in other blocks should remain unchanged
    assert ex_free.position == 0
    assert ex_other_block.position_in_block == 0

