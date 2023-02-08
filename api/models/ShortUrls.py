import boto3
import datetime
import os

client = boto3.client(
    "dynamodb",
    endpoint_url=(
        "http://dynamodb-local:8000" if os.environ.get("DYNAMODB_HOST", None) else None
    ),
    region_name="ca-central-1",
)

table = os.environ.get("TABLE_NAME", "url_shortener")


def create_short_url(original_url, short_url):
    response = client.put_item(
        TableName=table,
        Item={
            "short_url": {"S": short_url},
            "original_url": {"S": original_url},
            "click_count": {"N": "0"},
            "active": {"BOOL": True},
            "created": {"S": str(datetime.datetime.utcnow())},
        },
    )

    if response["ResponseMetadata"]["HTTPStatusCode"] == 200:
        return short_url
    else:
        return None


def get_short_url(short_url):
    response = client.get_item(
        TableName=table,
        Key={"short_url": {"S": short_url}},
        ProjectionExpression="short_url, original_url, click_count, active, created",
    )
    if response["ResponseMetadata"]["HTTPStatusCode"] == 200 and "Item" in response:
        return response["Item"]
    else:
        return None
