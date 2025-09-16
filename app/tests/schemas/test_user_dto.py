import pytest
from uuid import UUID
from app.schemas import UserCreate, UserRetrieve
from pydantic import ValidationError


def test_user_create(user: dict):

    user_dto = UserCreate(username=user.get("username"), password=user.get("password"))
    assert user_dto.username == "test-username123"
    assert user_dto.password == "test-password321"


def test_user_create_username_none(user: dict):

    with pytest.raises(ValidationError):
        UserCreate(username=None, password=user.get("password"))


def test_user_create_password_none(user: dict):

    with pytest.raises(ValidationError):
        UserCreate(username=user.get("username"), password=None)


def test_user_retrieve(user: dict, uuid4_fixture: UUID):

    UserRetrieve(uuid=user.get("uuid"), username=user.get("username"))


def test_user_retrieve_uuid_bad(user: dict, uuid4_fixture: UUID):

    bad_uuid = str(uuid4_fixture) + "123"

    with pytest.raises(ValidationError):
        UserRetrieve(uuid=bad_uuid, username=user.get("username"))
