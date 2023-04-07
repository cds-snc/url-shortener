import pytest
import os
import boto3
from fastapi.testclient import TestClient
from unittest import mock
from main import app


dynamodb_client = boto3.client(
    "dynamodb",
    endpoint_url=(os.environ.get("DYNAMODB_HOST", None)),
    region_name="ca-central-1",
)

table_name = os.environ.get("TABLE_NAME", "url_shortener_test")


@pytest.fixture(scope="session", autouse=True)
def setup_test_database():
    try:
        dynamodb_client.delete_table(TableName=table_name)
    except dynamodb_client.exceptions.ResourceNotFoundException:
        pass
    table = dynamodb_client.create_table(
        TableName=table_name,
        KeySchema=[
            {
                "AttributeName": "key_id",
                "KeyType": "HASH",
            }
        ],
        AttributeDefinitions=[
            {
                "AttributeName": "key_id",
                "AttributeType": "S",
            },
            {
                "AttributeName": "email",
                "AttributeType": "S",
            },
        ],
        GlobalSecondaryIndexes=[
            {
                "IndexName": "emailIndex",
                "KeySchema": [
                    {
                        "AttributeName": "email",
                        "KeyType": "HASH",
                    }
                ],
                "Projection": {
                    "ProjectionType": "ALL",
                },
                "ProvisionedThroughput": {
                    "ReadCapacityUnits": 1,
                    "WriteCapacityUnits": 1,
                },
            },
        ],
        ProvisionedThroughput={
            "ReadCapacityUnits": 1,
            "WriteCapacityUnits": 1,
        },
    )
    yield table
    dynamodb_client.delete_table(TableName=table_name)


@pytest.fixture(autouse=True)
def mock_settings_env_vars():
    with mock.patch.dict(
        os.environ,
        {
            "PEPPERS": "T4XuCG/uaDY7uHG+hG/01OOdgO77bl4GOdY5foLEHb8=,dPG6wEcrcOYc6lxqC/Hv3QD7CAHkzZ1wA0gZQW1kvkY=",
            "SHORTENER_PATH_LENGTH": "8",
        },
    ):
        yield


@pytest.fixture(scope="session")
def client() -> TestClient:
    yield TestClient(app)


@pytest.fixture(params=["en", "fr"])
def locale(request):
    return request.param


@pytest.fixture(params=["/en/login", "/fr/connexion"])
def login_path(request):
    return request.param


@pytest.fixture(params=["/en/logout", "/fr/deconnexion"])
def logout_path(request):
    return request.param


@pytest.fixture(params=["/en/magic-link", "/fr/lien-magique"])
def magic_link_path(request):
    return request.param
