from datetime import datetime
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)


def test_answers():
    # Создание ответа на несуществующий вопрос
    payload = {"text": "Ответ"}
    response = client.post(f"/questions/99999/answers/", json=payload)
    assert response.status_code == 404

    # Создание вопроса
    payload = {"text": "Вопрос не вопрос"}
    response = client.post("/questions/", json=payload)
    assert response.status_code == 200
    data = response.json()
    q_id = data["id"]

    # Создание пустого ответа
    payload = {"text": ""}
    response = client.post(f"/questions/{q_id}/answers/", json=payload)
    assert response.status_code == 422

    # Создание ответа с некорректным user_id
    payload = {"user_id": "It's me, Mario!", "text": "あなたは私を知っていますか？"}
    response = client.post(f"/questions/{q_id}/answers/", json=payload)
    assert response.status_code == 422

    # Создание первого ответа от нового пользователя
    payload = {"text": "Странный вопрос..."}
    response = client.post(f"/questions/{q_id}/answers/", json=payload)
    data = response.json()
    answer_id = data["id"]
    user_id = data["user_id"]  # Сохраняем ID пользователя на будущее

    # Просмотр ответа
    response = client.get(f"/answers/{answer_id}")
    assert response.status_code == 200
    data = response.json()
    assert data["question_id"] == q_id
    assert data["user_id"] == user_id
    assert data["text"] == "Странный вопрос..."
    assert datetime.fromisoformat(data["created_at"])

    # Удаление ответа
    response = client.delete(f"/answers/{answer_id}")
    assert response.status_code == 200
    response = client.get(f"/answers/{answer_id}")
    assert response.status_code == 404
    
    # Создание ответов от имеющегося пользователя
    for answer in ("Да", "Нет", "Наверное"):
        payload = {"user_id": user_id, "text": answer}
        response = client.post(f"/questions/{q_id}/answers/", json=payload)
        data = response.json()
    
    # Проверка ответов
    response = client.get(f"/questions/{q_id}")
    assert response.status_code == 200
    data = response.json()
    answers = data["answers"]
    assert len(answers) == 3
    assert answers[0]["text"] == "Да"
    assert answers[1]["text"] == "Нет"
    assert answers[2]["text"] == "Наверное"
    # Совпадение user_id
    assert answers[0]["user_id"] == answers[1]["user_id"] == answers[2]["user_id"]

    # Проверка каскадного удаления ответов
    ids = [answers[i]["id"] for i in range(3)]
    response = client.delete(f"/questions/{q_id}")
    assert response.status_code == 200
    for id in ids:
        response = client.get(f"/answers/{id}")
        assert response.status_code == 404
