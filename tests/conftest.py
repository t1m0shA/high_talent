import pytest
from uuid import uuid4, UUID
from datetime import datetime
from sqlalchemy.orm import Session
from app.db import get_db
from app.db.base import Base
from sqlalchemy import text


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


@pytest.fixture(scope="function")
def db_session():

    session: Session = next(get_db())

    try:
        yield session

    finally:

        session.execute(text("SET session_replication_role = 'replica';"))
        try:
            for table in reversed(Base.metadata.sorted_tables):
                session.execute(table.delete())
            session.commit()
        finally:
            session.execute(text("SET session_replication_role = 'origin';"))
            session.close()
