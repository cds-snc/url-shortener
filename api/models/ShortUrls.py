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


def create_short_url(original_url, short_url):
    # Expire an url after 2 years in epoch time
    two_years_time = datetime.datetime.today() + datetime.timedelta(days=(365 * 2))
    expiry_date = int(time.mktime(two_years_time.timetuple()))
    response = client.put_item(
        TableName=table,
        Item={
            "short_url": {"S": short_url},
            "original_url": {"S": original_url},
            "click_count": {"N": "0"},
            "active": {"BOOL": True},
            "created": {"S": str(datetime.datetime.utcnow())},
            "ttl": {"N": str(expiry_date)},
        },
    )

    if response["ResponseMetadata"]["HTTPStatusCode"] == 200:
        return short_url
    else:
        return None


def get_short_url(short_url):
    # AWS does not delete expired items immediately (typically deletes within 48 hours) so we still need to sure we don't return any expired urls
    epochTimeNow = int(time.time())
    response = client.query(
        TableName=table,
        KeyConditionExpression="#short_url = :short_url",
        FilterExpression="#t > :ttl",
        ExpressionAttributeNames={"#t": "ttl", "#short_url": "short_url"},
        ExpressionAttributeValues={
            ":ttl": {
                "N": str(epochTimeNow),
            },
            ":short_url": {"S": short_url},
        },
    )
    if (
        response["ResponseMetadata"]["HTTPStatusCode"] == 200
        and "Items" in response
        and len(response["Items"]) > 0
    ):
        return response["Items"][0]
    else:
        return None
