# Tests that the home page loads and shows the dashboard

from web_app import app

def test_home_page():
    # Use Flask's built-in test client
    client = app.test_client()
    resp = client.get("/")

    assert resp.status_code == 200
    assert b"Emotion History" in resp.data
