import boto3
import datetime
import time
import os
import uuid

client = boto3.client(
    "dynamodb",
    endpoint_url=(os.environ.get("DYNAMODB_HOST", None)),
    region_name="ca-central-1",
)

table = os.environ.get("TABLE_NAME", "url_shortener")

MODEL_PREFIX = "EMAIL_LINK"


def create(email):
    guid = str(uuid.uuid4())
    timestamp = int(datetime.datetime.utcnow().timestamp())
    response = client.put_item(
        TableName=table,
        Item={
            "key_id": {"S": f"{MODEL_PREFIX}/{guid}"},
            "email": {"S": f"{MODEL_PREFIX}/{email}"},
            "created_at": {"N": str(timestamp)},
            "ttl": {"N": str(timestamp + (60 * 5))},  # 5 mins
        },
    )
    if response["ResponseMetadata"]["HTTPStatusCode"] == 200:
        return [guid, email]
    else:
        return [None, None]


def delete(composite_key):
    response = client.delete_item(
        TableName=table,
        Key={"key_id": {"S": f"{MODEL_PREFIX}/{composite_key}"}},
    )
    if response["ResponseMetadata"]["HTTPStatusCode"] == 200:
        return True
    else:
        return False


def get(guid):
    epoch_time_now = int(time.time())
    response = client.get_item(
        TableName=table,
        Key={"key_id": {"S": f"{MODEL_PREFIX}/{guid}"}},
        ProjectionExpression="email",
    )
    if response["ResponseMetadata"]["HTTPStatusCode"] == 200 and "Item" in response:
        if (
            "ttl" in response["Item"]
            and int(response["Item"]["ttl"]["N"]) < epoch_time_now
        ):
            delete(guid)
            return None
        return response["Item"]["email"]["S"].split("/").pop()
    else:
        return None


def check_if_exists(email):
    epoch_time_now = int(time.time())
    response = client.query(
        TableName=table,
        IndexName="emailIndex",
        KeyConditionExpression="email = :email",
        FilterExpression="#t > :ttl",
        ExpressionAttributeNames={"#t": "ttl", "#email": "email"},
        ExpressionAttributeValues={
            ":email": {"S": f"{MODEL_PREFIX}/{email}"},
            ":ttl": {"N": str(epoch_time_now)},
        },
    )
    if (
        response["ResponseMetadata"]["HTTPStatusCode"] == 200
        and "Items" in response
        and len(response["Items"]) > 0
    ):
        return True
    else:
        return False
