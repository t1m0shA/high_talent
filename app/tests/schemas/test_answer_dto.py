import pytest
from app.schemas import AnswerCreate, AnswerRetrieve
from pydantic import ValidationError


def test_answer_create(answer: dict, question: dict):

    answer_dto = AnswerCreate(text=answer.get("text"), question_id=question.get("id"))
    assert answer_dto.text == "Test answer text"
    assert answer_dto.question_id == 12


def test_answer_create_text_none():

    with pytest.raises(ValidationError):
        AnswerCreate(text=None, question_id=14)


def test_answer_create_question_id_none():

    with pytest.raises(ValidationError):
        AnswerCreate(text="Test answer text", question_id=None)


def test_answer_retrieve(answer: dict, question: dict, user: dict):

    AnswerRetrieve(
        id=answer.get("id"),
        text=answer.get("text"),
        question=question,
        user=user,
        created_at=question.get("created_at"),
    )
