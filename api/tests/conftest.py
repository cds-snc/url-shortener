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
                "AttributeName": "short_url",
                "KeyType": "HASH",
            },
        ],
        AttributeDefinitions=[
            {
                "AttributeName": "short_url",
                "AttributeType": "S",
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
            "PEPPERS": "T4XuCG/uaDY7uHG+hG/01OOdgO77bl4GOdY5foLEHb8=,dPG6wEcrcOYc6lxqC/Hv3QD7CAHkzZ1wA0gZQW1kvkY="
        },
    ):
        yield


@pytest.fixture(scope="session")
def client() -> TestClient:
    yield TestClient(app)
