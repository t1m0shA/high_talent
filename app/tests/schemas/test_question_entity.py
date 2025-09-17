import pytest
from app.schemas import Question, Answer
from app.errors import QuestionSchemaError


def test_question_entity(question: dict, answer: dict):

    question_entity = Question(**question)
    answer_entity = Answer(**answer)

    assert question_entity.id == 12
    assert question_entity.text == "Test question text?"
    assert question_entity.answers == [answer_entity]


def test_question_entity_text_empty(question: dict):

    question_data = question.copy()
    question_data.update({"text": ""})

    with pytest.raises(QuestionSchemaError):
        Question(**question_data)
