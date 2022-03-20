import pytest
from fastapi.testclient import TestClient

from main import app

@pytest.fixture()
def client() -> TestClient: 
    client = TestClient(app)
    yield client
