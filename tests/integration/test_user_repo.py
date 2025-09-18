import pytest
from uuid import uuid4
from app.db.models import User
from app.db import UserRepository
from app.core.security import get_password_hash


@pytest.fixture
def user_repo(db_session):
    return UserRepository(db_session)


def test_create_userr(user_repo):

    username = "testuser"
    password_hash = get_password_hash("password123")
    user = user_repo.create(username=username, password_hash=password_hash)

    assert user.uuid is not None
    assert user.username == username
    assert user.password_hash != "password123"


def test_get_by_username(user_repo):

    username = "bob"
    password_hash = get_password_hash("secret")
    user_repo.create(username=username, password_hash=password_hash)

    user = user_repo.get_by_username(username)
    assert user is not None
    assert user.username == username


def test_get_by_uuid(user_repo):

    username = "tim"
    password_hash = get_password_hash("secret")
    created_user = user_repo.create(username=username, password_hash=password_hash)

    user = user_repo.get_by_uuid(created_user.uuid)
    assert user is not None
    assert user.uuid == created_user.uuid
