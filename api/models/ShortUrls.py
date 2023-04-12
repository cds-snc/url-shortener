import boto3
import botocore
import datetime
import time
import os

client = boto3.client(
    "dynamodb",
    endpoint_url=(os.environ.get("DYNAMODB_HOST", None)),
    region_name="ca-central-1",
)

table = os.environ.get("TABLE_NAME", "url_shortener")

MODEL_PREFIX = "URL"


def create_short_url(original_url, short_url, created_by):
    """
    create_short_url creates a new entry with short_url as key.
    If an entry already exists, the original_url is compared.
    If the original_url(s) are the same, then this is a no-op, and
    the shortened URL is returned.
    Otherwise, this is a collision and a ValueError exception is raised.
    The caller should try again with a new short_url.
    parameter original_url: the url that the user passes to the api
    parameter short_url: short url mapped to the original url

    returns: shortened url
    """
    # Expire an url after 2 years in epoch time
    two_years_time = datetime.datetime.today() + datetime.timedelta(days=(365 * 2))
    expiry_date = int(time.mktime(two_years_time.timetuple()))
    try:
        response = client.put_item(
            TableName=table,
            Item={
                "key_id": {"S": f"{MODEL_PREFIX}/{short_url}"},
                "original_url": {"S": original_url},
                "click_count": {"N": "0"},
                "active": {"BOOL": True},
                "created_at": {"N": str(int(datetime.datetime.utcnow().timestamp()))},
                "created_by": {"S": created_by},
                "ttl": {"N": str(expiry_date)},
            },
            ConditionExpression="attribute_not_exists(key_id)",
        )
        if response["ResponseMetadata"]["HTTPStatusCode"] != 200:
            raise RuntimeError(response)
    except botocore.exceptions.ClientError as err:
        if err.response["Error"]["Code"] == "ConditionalCheckFailedException":
            # key already exists
            # if value (original url) does not match, this is a collision
            # otherwise no-op
            if get_short_url(short_url)["original_url"]["S"] != original_url:
                raise ValueError(f"Key exists: {short_url}")
        else:
            raise

    return short_url


def get_short_url(short_url):
    """
    get_short_url returns original_url for a given short_url.
    parameter short_url: short url mapped to the original url

    returns: response object containing original url.
    """
    # AWS does not delete expired items immediately (typically deletes within 48 hours)
    # so we still need to sure we don't return any expired urls
    epoch_time_now = int(time.time())
    response = client.query(
        TableName=table,
        KeyConditionExpression="#key_id = :key_id",
        FilterExpression="#t > :ttl",
        ExpressionAttributeNames={"#t": "ttl", "#key_id": "key_id"},
        ExpressionAttributeValues={
            ":ttl": {
                "N": str(epoch_time_now),
            },
            ":key_id": {"S": f"{MODEL_PREFIX}/{short_url}"},
        },
    )
    if (
        response["ResponseMetadata"]["HTTPStatusCode"] == 200
        and "Items" in response
        and len(response["Items"]) > 0
    ):
        # Update the URL's click count
        client.update_item(
            TableName=table,
            Key={"key_id": {"S": f"{MODEL_PREFIX}/{short_url}"}},
            UpdateExpression="SET click_count = click_count + :val",
            ExpressionAttributeValues={":val": {"N": "1"}},
        )
        return response["Items"][0]
    else:
        return None
