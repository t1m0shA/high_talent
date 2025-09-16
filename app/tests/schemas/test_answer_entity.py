import pytest
from app.schemas import Answer, User
from app.errors import AnswerError


def test_answer_entity(answer: dict, user: dict):

    answer_entity = Answer(**answer)
    user_entity = User(**user)

    assert answer_entity.id == 17
    assert answer_entity.text == "Test answer text"
    assert answer_entity.user == user_entity


def test_answer_entity_text_empty(answer: dict):

    answer_data = answer.copy()
    answer_data.update({"text": ""})

    with pytest.raises(AnswerError):
        Answer(**answer_data)
