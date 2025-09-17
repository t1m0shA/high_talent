import pytest
from app.schemas import QuestionCreate, QuestionRetrieve
from pydantic import ValidationError


def test_question_create(question: dict):

    question_dto = QuestionCreate(text=question.get("text"))
    assert question_dto.text == "Test question text?"


def test_question_create_text_none():

    with pytest.raises(ValidationError):
        QuestionCreate(text=None)


def test_question_retrieve(question: dict):

    QuestionRetrieve(
        id=question.get("id"),
        text=question.get("text"),
        created_at=question.get("created_at"),
        answers=[],
    )
