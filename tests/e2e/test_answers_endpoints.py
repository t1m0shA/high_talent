import pytest
from fastapi.testclient import TestClient
from datetime import datetime
from app.main import app
from app.db.models import User, Question, Answer
from app.api.deps import get_current_user

client = TestClient(app)


@pytest.fixture
def create_user(db_session):

    user = User(username="testuser", password_hash="fakehash")
    db_session.add(user)
    db_session.commit()
    db_session.refresh(user)

    return user


@pytest.fixture
def create_question(db_session):

    question = Question(text="Test question", created_at=datetime.now())
    db_session.add(question)
    db_session.commit()
    db_session.refresh(question)

    return question


@pytest.fixture
def create_answer(db_session, create_user, create_question):

    answer = Answer(
        text="Test answer",
        user_id=create_user.uuid,
        question_id=create_question.id,
        created_at=datetime.now(),
    )

    db_session.add(answer)
    db_session.commit()
    db_session.refresh(answer)

    return answer


@pytest.fixture
def override_get_current_user(create_user):

    def _override():
        return create_user.username

    app.dependency_overrides[get_current_user] = _override
    yield
    app.dependency_overrides.clear()


def test_get_answer(create_answer):

    answer_id = create_answer.id
    response = client.get(f"/answers/{answer_id}")
    assert response.status_code == 200

    data = response.json()

    assert data["text"] == create_answer.text
    assert data["id"] == create_answer.id


def test_delete_answer_success(create_answer, override_get_current_user):

    answer_id = create_answer.id
    response = client.delete(f"/answers/{answer_id}")
    assert response.status_code == 204

    from app.db import get_db

    db = next(get_db())
    deleted = db.query(Answer).filter(Answer.id == answer_id).first()

    assert deleted is None


def test_delete_answer_wrong_user(create_answer):

    def fake_user():
        return "anotheruser"

    app.dependency_overrides[get_current_user] = fake_user

    response = client.delete(f"/answers/{create_answer.id}")
    assert response.status_code == 404

    app.dependency_overrides.clear()
