import pytest
from app.schemas import AnswerCreate, AnswerRetrieve
from pydantic import ValidationError


def test_answer_create(answer: dict, question: dict):

    answer_dto = AnswerCreate(text=answer.get("text"))
    assert answer_dto.text == "Test answer text"


def test_answer_create_text_none():

    with pytest.raises(ValidationError):
        AnswerCreate(text=None)


def test_answer_retrieve(answer: dict, question: dict, user: dict):

    AnswerRetrieve(
        id=answer.get("id"),
        text=answer.get("text"),
        question=question,
        user=user,
        created_at=question.get("created_at"),
    )
