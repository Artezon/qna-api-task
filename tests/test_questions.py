from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)


def test_get_questions():
    response = client.get("/questions/?page=1&count=5")
    assert response.status_code == 200
    data = response.json()
    assert "data" in data
    assert data["page"] == 1
    assert data["count"] == 5


def test_get_questions_missing_page():
    response = client.get("/questions/?page=1000")
    assert response.status_code == 200
    data = response.json()
    assert len(data["data"]) == 0


def test_post_question():
    payload = {"text": "Что такое доброта?"}
    response = client.post("/questions/", json=payload)
    assert response.status_code == 200
    data = response.json()
    assert data["text"] == payload["text"]
    assert "id" in data


def test_post_empty_question():
    payload = {"text": ""}
    response = client.post("/questions/", json=payload)
    assert response.status_code == 422


def test_get_question_by_id():
    payload = {"text": "Что лучше - 🐧 или 🪟?"}
    post_response = client.post("/questions/", json=payload)
    question_id = post_response.json()["id"]

    get_response = client.get(f"/questions/{question_id}")
    assert get_response.status_code == 200
    data = get_response.json()
    assert data["id"] == question_id
    assert data["text"] == payload["text"]
    assert data["answers"] == []


def test_get_nonexistent_question():
    response = client.get("/questions/99999")
    assert response.status_code == 404
