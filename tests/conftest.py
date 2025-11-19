import os
import pytest
from web_app.app import app  # <-- CORRECT IMPORT

@pytest.fixture
def client():
    os.environ["TESTING"] = "1"
    app.config["TESTING"] = True
    with app.test_client() as client:
        yield client
