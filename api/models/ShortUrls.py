import boto3
import datetime
import os

client = boto3.client(
    "dynamodb",
    endpoint_url=(os.environ.get("DYNAMODB_HOST", None)),
    region_name="ca-central-1",
)

table = os.environ.get("TABLE_NAME", "url_shortener")

MODEL_PREFIX = "URL"


def create_short_url(original_url, short_url):
    response = client.put_item(
        TableName=table,
        Item={
            "key_id": {"S": f"{MODEL_PREFIX}/{short_url}"},
            "created_at": {"N": str(int(datetime.datetime.utcnow().timestamp()))},
            "original_url": {"S": original_url},
            "click_count": {"N": "0"},
            "active": {"BOOL": True},
        },
    )

    if response["ResponseMetadata"]["HTTPStatusCode"] == 200:
        return short_url
    else:
        return None


def get_short_url(short_url):
    response = client.get_item(
        TableName=table,
        Key={"key_id": {"S": f"{MODEL_PREFIX}/{short_url}"}},
        ProjectionExpression="key_id, original_url, click_count, active, created_at",
    )
    if response["ResponseMetadata"]["HTTPStatusCode"] == 200 and "Item" in response:
        return response["Item"]
    else:
        return None
