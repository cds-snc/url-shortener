import os
from fastapi.testclient import TestClient
from unittest.mock import patch
import main

client = TestClient(main.app)


# Test that the version endpoint returns unknown if the GIT_SHA environment variable is not set
def test_version_with_no_GIT_SHA():
    response = client.get("/version")
    assert response.status_code == 200
    assert response.json() == {"version": "unknown"}


# Test that the version endpoint returns the GIT_SHA environment variable if it is set
@patch.dict(os.environ, {"GIT_SHA": "foo"}, clear=True)
def test_version_with_GIT_SHA():
    response = client.get("/version")
    assert response.status_code == 200
    assert response.json() == {"version": "foo"}
