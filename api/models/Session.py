import boto3
import datetime
import time
import os

client = boto3.client(
    "dynamodb",
    endpoint_url=(os.environ.get("DYNAMODB_HOST", None)),
    region_name="ca-central-1",
)

table = os.environ.get("TABLE_NAME", "url_shortener")

MODEL_PREFIX = "SESSION"


def create(session_id, data):
    """Create a new session."""
    timestamp = int(datetime.datetime.utcnow().timestamp())
    response = client.put_item(
        TableName=table,
        Item={
            "key_id": {"S": f"{MODEL_PREFIX}/{session_id}"},
            "created_at": {"N": str(timestamp)},
            "ttl": {"N": str(timestamp + (60 * 60 * 2))},  # 2 hours
            "session_data": {"S": data},
        },
    )

    if response["ResponseMetadata"]["HTTPStatusCode"] == 200:
        return session_id
    else:
        return False


def read(session_id):
    """Read session data."""
    epoch_time_now = int(time.time())
    response = client.get_item(
        TableName=table,
        Key={"key_id": {"S": f"{MODEL_PREFIX}/{session_id}"}},
    )
    if response["ResponseMetadata"]["HTTPStatusCode"] == 200 and "Item" in response:
        if (
            "ttl" in response["Item"]
            and int(response["Item"]["ttl"]["N"]) < epoch_time_now
        ):
            delete(session_id)
            return None
        return response["Item"]
    else:
        return None


def delete(session_id):
    """Delete session data."""
    response = client.delete_item(
        TableName=table,
        Key={"key_id": {"S": f"{MODEL_PREFIX}/{session_id}"}},
    )

    if response["ResponseMetadata"]["HTTPStatusCode"] == 200:
        return session_id
    else:
        return None
