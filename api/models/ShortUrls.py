import boto3
import botocore
import datetime
import os

client = boto3.client(
    "dynamodb",
    endpoint_url=(os.environ.get("DYNAMODB_HOST", None)),
    region_name="ca-central-1",
)

table = os.environ.get("TABLE_NAME", "url_shortener")


def create_short_url(original_url, short_url):
    try:
        response = client.put_item(
            TableName=table,
            Item={
                "short_url": {"S": short_url},
                "original_url": {"S": original_url},
                "click_count": {"N": "0"},
                "active": {"BOOL": True},
                "created": {"S": str(datetime.datetime.utcnow())},
            },
            ConditionExpression='attribute_not_exists(short_url)'
        )
        if response["ResponseMetadata"]["HTTPStatusCode"] != 200:
            raise RuntimeError(response)
    except botocore.exceptions.ClientError as err:
        if err.response['Error']['Code'] == 'ConditionalCheckFailedException':
            # key already exists
            # if value (original url) does not match, this is a collision
            # otherwise no-op
            if get_short_url(short_url)['original_url']['S'] != original_url:
                raise ValueError(f"Key exists: {short_url}")
        else:
            raise

    return short_url


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
