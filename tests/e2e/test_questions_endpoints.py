import pytest
from fastapi.testclient import TestClient
from datetime import datetime
from app.main import app
from app.db.models import Question

client = TestClient(app)


@pytest.fixture
def question_payload():
    return {"text": "What is the meaning of life?"}


def test_create_question(db_session, question_payload):

    response = client.post("/questions/", json=question_payload)
    assert response.status_code == 201

    data = response.json()
    assert data["text"] == question_payload["text"]
    assert "id" in data


def test_list_questions(db_session, question_payload):

    client.post("/questions/", json=question_payload)

    response = client.get("/questions/")
    assert response.status_code == 200

    data = response.json()
    assert len(data) == 1
    assert data[0]["text"] == question_payload["text"]


def test_get_question(db_session, question_payload):

    create_resp = client.post("/questions/", json=question_payload)
    question_id = create_resp.json()["id"]

    response = client.get(f"/questions/{question_id}")
    assert response.status_code == 200

    data = response.json()
    assert data["id"] == question_id
    assert data["text"] == question_payload["text"]


def test_delete_question(db_session, question_payload):

    create_resp = client.post("/questions/", json=question_payload)
    question_id = create_resp.json()["id"]

    del_resp = client.delete(f"/questions/{question_id}")
    assert del_resp.status_code == 204

    get_resp = client.get(f"/questions/{question_id}")
    assert get_resp.status_code == 404
