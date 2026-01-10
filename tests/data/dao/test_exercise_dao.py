from unittest.mock import MagicMock
from src.data.models import Exercise, ExerciseType, Block

def test_create(exercise_dao, mock_dbs):
    mock_db = mock_dbs['exercise']
    exercise = Exercise(
        exercise_type=ExerciseType.air_squat,
        session_id=1,
        block_id=None,
        position=0,
        position_in_block=None,
        weight_kg=None,
        repetitions=10,
        duration_seconds=None,
        distance_meters=None,
        notes="Test exercise"
    )
    result = exercise_dao.create(exercise)
    mock_db.add.assert_called_once_with(exercise)
    mock_db.commit.assert_called_once()
    mock_db.refresh.assert_called_once_with(exercise)
    assert result == exercise

def test_get_by_id(exercise_dao, mock_dbs):
    mock_db = mock_dbs['exercise']
    mock_db.get.return_value = "found"
    result = exercise_dao.get_by_id(1)
    mock_db.get.assert_called_once_with(Exercise, 1)
    assert result == "found"

def test_list_by_session(exercise_dao, mock_dbs):
    mock_db = mock_dbs['exercise']
    mock_scalars = MagicMock()
    mock_scalars.__iter__.return_value = iter(["e1", "e2"])  # <-- ici
    mock_db.scalars.return_value = mock_scalars
    result = exercise_dao.list_by_session(1)
    mock_db.scalars.assert_called_once()
    assert result == ["e1", "e2"]

def test_list_by_block(exercise_dao, mock_dbs):
    mock_db = mock_dbs['exercise']
    mock_scalars = MagicMock()
    mock_scalars.__iter__.return_value = iter(["e1", "e2"])  # <-- ici
    mock_db.scalars.return_value = mock_scalars
    result = exercise_dao.list_by_block(2)
    mock_db.scalars.assert_called_once()
    assert result == ["e1", "e2"]

def test_update(exercise_dao, mock_dbs):
    mock_db = mock_dbs['exercise']
    exercise = MagicMock()
    result = exercise_dao.update(exercise)
    mock_db.commit.assert_called_once()
    mock_db.refresh.assert_called_once_with(exercise)
    assert result == exercise

def test_delete(exercise_dao, mock_dbs):
    mock_db = mock_dbs['exercise']
    exercise = MagicMock()
    exercise_dao.delete(exercise)
    mock_db.delete.assert_called_once_with(exercise)
    mock_db.commit.assert_called_once()

def test_validate_block_session_true(exercise_dao, mock_dbs):
    mock_db = mock_dbs['exercise']
    block = MagicMock()
    block.session_id = 1
    mock_db.get.return_value = block
    result = exercise_dao.validate_block_session(2, 1)
    mock_db.get.assert_called_once_with(Block, 2)
    assert result is True

def test_validate_block_session_false(exercise_dao, mock_dbs):
    mock_db = mock_dbs['exercise']
    mock_db.get.return_value = None
    result = exercise_dao.validate_block_session(2, 1)
    mock_db.get.assert_called_once_with(Block, 2)
    assert result is False

def test_count_free_by_session(exercise_dao, mock_dbs):
    mock_db = mock_dbs["exercise"]

    mock_scalars = MagicMock()
    mock_scalars.one.return_value = 3
    mock_db.scalars.return_value = mock_scalars

    result = exercise_dao.count_free_by_session(1)
    assert result == 3


def test_count_by_block(exercise_dao, mock_dbs):
    mock_db = mock_dbs["exercise"]

    mock_scalars = MagicMock()
    mock_scalars.one.return_value = 4
    mock_db.scalars.return_value = mock_scalars

    result = exercise_dao.count_by_block(2)
    assert result == 4



