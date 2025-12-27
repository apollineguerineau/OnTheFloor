from src.data.dao.user_dao import UserDAO
from src.data.models import User

def test_create_user(db_session):
    dao = UserDAO(db_session)

    user = dao.create(username="john")

    assert user.id is not None
    assert str(user.username) == "john"


def test_get_user_by_username(db_session):
    dao = UserDAO(db_session)
    dao.create(username="alice")

    user = dao.get_by_username("alice")

    assert user is not None
    assert str(user.username) == "alice"


def test_get_user_not_found(db_session):
    dao = UserDAO(db_session)

    user = dao.get_by_username("ghost")
    assert user is None
