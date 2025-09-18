import pytest
from datetime import datetime
from app.db import QuestionRepository, Question, get_db
from app.schemas import Question as QuestionSchema
from app.errors import QuestionNotFoundDbError


@pytest.fixture
def repo(db_session):

    return QuestionRepository(db_session)


def test_create_question(repo, db_session):

    question_data = QuestionSchema(
        text="What is Python?", created_at=datetime.now(), answers=[]
    )
    created = repo.create(question_data)

    assert created.id is not None
    assert created.text == question_data.text

    db_question = db_session.query(Question).filter(Question.id == created.id).first()
    assert db_question is not None
    assert db_question.text == "What is Python?"


def test_get_by_id(repo, db_session):

    question_data = QuestionSchema(
        text="What is FastAPI?", created_at=datetime.now(), answers=[]
    )
    created = repo.create(question_data)

    fetched = repo.get_by_id(created.id)
    assert fetched is not None
    assert fetched.text == "What is FastAPI?"


def test_list_all(repo, db_session):

    db_session.query(Question).delete()
    db_session.commit()

    questions = [
        QuestionSchema(text="Q1", created_at=datetime.now(), answers=[]),
        QuestionSchema(text="Q2", created_at=datetime.now(), answers=[]),
    ]

    for q in questions:
        repo.create(q)

    all_questions = repo.list_all()
    assert len(all_questions) == 2
    assert all_questions[0].text == "Q1"
    assert all_questions[1].text == "Q2"


def test_delete_question(repo, db_session):

    question_data = QuestionSchema(
        text="To be deleted?", created_at=datetime.now(), answers=[]
    )
    created = repo.create(question_data)

    repo.delete(created.id)

    deleted = db_session.query(Question).filter(Question.id == created.id).first()
    assert deleted is None


def test_delete_nonexistent_question_raises(repo):

    with pytest.raises(QuestionNotFoundDbError):
        repo.delete(9999)
