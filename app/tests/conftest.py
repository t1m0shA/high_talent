import pytest
from uuid import uuid4, UUID
from datetime import datetime


@pytest.fixture
def uuid4_fixture() -> UUID:

    return uuid4()


@pytest.fixture
def user(uuid4_fixture) -> dict:

    return {
        "uuid": uuid4_fixture,
        "username": "test-username123",
        "password": "test-password321",
    }


@pytest.fixture
def answer(user) -> dict:

    return {
        "id": 17,
        "text": "Test answer text",
        "user": user,
        "created_at": datetime.now(),
    }


@pytest.fixture
def question(answer) -> dict:

    return {
        "id": 12,
        "text": "Test question text?",
        "created_at": datetime.now(),
        "answers": [answer],
    }
