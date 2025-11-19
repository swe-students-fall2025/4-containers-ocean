# tests/test_app.py

def test_homepage_loads(client):
    response = client.get("/")
    assert response.status_code == 200


def test_upload_without_file(client):
    response = client.post("/upload")
    assert response.status_code == 400
    assert b"No audio file provided" in response.data


def test_emotion_history_json(client):
    response = client.get("/history-json")  # <-- FIXED ENDPOINT
    assert response.status_code == 200
    assert isinstance(response.json, dict)
