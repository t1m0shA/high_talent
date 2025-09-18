import pytest
from app.schemas import User
from app.errors import UserEmptyUsernameError, UserEmptyPasswordError
from pydantic import ValidationError
from uuid import UUID


def test_user_entity(user: dict, uuid4_fixture: UUID):

    user_entity = User(**user)
    assert user_entity.uuid == uuid4_fixture
    assert user_entity.username == "test-username123"
    assert user_entity.password == "test-password321"


def test_user_entity_username_empty(uuid4_fixture: UUID):

    with pytest.raises(UserEmptyUsernameError):
        User(uuid=uuid4_fixture, username="", password=str(uuid4_fixture))


def test_user_entity_username_short(uuid4_fixture: UUID):

    with pytest.raises(UserEmptyUsernameError):
        User(uuid=uuid4_fixture, username="ar", password=str(uuid4_fixture))


def test_user_entity_username_minimum(uuid4_fixture: UUID):

    User(uuid=uuid4_fixture, username="usr", password=str(uuid4_fixture))


def test_user_entity_password_empty(user: dict, uuid4_fixture: UUID):

    with pytest.raises(UserEmptyPasswordError):
        User(uuid=uuid4_fixture, username=user.get("username"), password="")


def test_user_entity_password_none(user: dict, uuid4_fixture: UUID):

    User(uuid=uuid4_fixture, username=user.get("username"), password=None)
