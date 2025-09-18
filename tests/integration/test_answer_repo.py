import pytest
from datetime import datetime
from app.db.models import Answer, Question, User
from app.db import AnswerRepository, QuestionRepository, UserRepository
from app.schemas import Answer as AnswerSchema, Question as QuestionSchema
from app.errors import AnswerNotFoundDbError


@pytest.fixture
def user(db_session):

    repo = UserRepository(db_session)
    return repo.create(username="testuser", password_hash="hashed_pw")


@pytest.fixture
def question(db_session):

    repo = QuestionRepository(db_session)
    q_schema = QuestionSchema(
        text="Test question", created_at=datetime.now(), answers=[]
    )
    return repo.create(q_schema)


@pytest.fixture
def answer_repo(db_session):

    return AnswerRepository(db_session)


def test_create_answer(db_session, user, question, answer_repo):

    answer_schema = AnswerSchema(
        text="Test answer", user=user, created_at=datetime.now()
    )
    created = answer_repo.create(answer_schema, question)

    assert created.id is not None
    assert created.text == "Test answer"
    assert created.user_id == user.uuid
    assert created.question_id == question.id


def test_get_by_id(db_session, user, question, answer_repo):

    answer_schema = AnswerSchema(
        text="Another answer", user=user, created_at=datetime.now()
    )
    created = answer_repo.create(answer_schema, question)

    fetched = answer_repo.get_by_id(created.id)
    assert fetched.id == created.id
    assert fetched.text == created.text


def test_delete_answer(db_session, user, question, answer_repo):

    answer_schema = AnswerSchema(
        text="To be deleted", user=user, created_at=datetime.now()
    )
    created = answer_repo.create(answer_schema, question)

    answer_repo.delete(created.id)
    assert answer_repo.get_by_id(created.id) is None


def test_delete_nonexistent_answer_raises(db_session, answer_repo):

    with pytest.raises(AnswerNotFoundDbError):
        answer_repo.delete(999)
