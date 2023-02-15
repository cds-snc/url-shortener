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




# Test that the healthcheck endpoint returns ERROR if the dynanoDB is down
@patch("routers.ops.is_db_up")
def test_healthcheck_failure(db_mock):
   db_mock.return_value = False
   response = client.get("/healthcheck")
   assert response.status_code == 200
   expected_val = {
       "status": "ERROR",
       "message": "Not able to connect to the database",
   }
   assert response.json() == expected_val




# Test that the healthcheck endpoint returns OK if the dynanoDB is up
@patch("routers.ops.is_db_up")
def test_healthcheck_success(db_mock):
   db_mock.return_value = True
   response = client.get("/healthcheck")
   assert response.status_code == 200
   expected_val = {"status": "OK", "message": "Able to connect to the database"}
   assert response.json() == expected_val
