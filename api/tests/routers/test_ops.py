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


# Test that the healthcheck endpoint returns an error when the dynamoDB host is empty
@patch.dict(os.environ, {"DYNAMODB_HOST": ""}, clear=True)
def test_healthcheck_failure_host_empty():
    response = client.get("/healthcheck")
    assert response.status_code == 200
    expected_val = {
        "status": "ERROR",
        "message": "Not able to connect to the database",
    }
    assert response.json() == expected_val


# Test that the healthcheck endpoint returns an error when the dynamoDB host provided is wrong
@patch.dict(os.environ, {"DYNAMODB_HOST": "foo_db"}, clear=True)
def test_healthcheck_failure_wrong_host():
    response = client.get("/healthcheck")
    assert response.status_code == 200
    expected_val = {
        "status": "ERROR",
        "message": "Not able to connect to the database",
    }
    assert response.json() == expected_val


# Test that the healthcheck endpoint returns an error when the table name provided is empty
@patch.dict(os.environ, {"TABLE_NAME": ""}, clear=True)
def test_healthcheck_failure_empty_table_name():
    response = client.get("/healthcheck")
    assert response.status_code == 200
    expected_val = {
        "status": "ERROR",
        "message": "Not able to connect to the database",
    }
    assert response.json() == expected_val


# Test that the healthcheck endpoint returns an error when the table name provided is wrong
@patch.dict(os.environ, {"TABLE_NAME": "foo"}, clear=True)
def test_healthcheck_failure_wrong_table_name():
    response = client.get("/healthcheck")
    assert response.status_code == 200
    expected_val = {
        "status": "ERROR",
        "message": "Not able to connect to the database",
    }
    assert response.json() == expected_val


# Test that the healthcheck endpoint returns an error if the dynamoDB table and host is wrong
@patch.dict(os.environ, {"DYNAMODB_HOST": "foo_db", "TABLE_NAME": "foo"}, clear=True)
def test_healthcheck_failure_wrong_host_and_table():
    response = client.get("/healthcheck")
    assert response.status_code == 200
    expected_val = {
        "status": "ERROR",
        "message": "Not able to connect to the database",
    }
    assert response.json() == expected_val


# # Test that the healthcheck endpoint returns OK if the host and table name are right and all is good.
def test_healthcheck_success():
    response = client.get("/healthcheck")
    assert response.status_code == 200
    expected_val = {"status": "OK", "message": "Able to connect to the database"}
    assert response.json() == expected_val
