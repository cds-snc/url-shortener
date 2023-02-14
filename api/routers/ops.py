"""
API routes for for operational and status requests
"""
from os import environ
from fastapi import APIRouter
import boto3
import botocore


router = APIRouter()


# Return the current version of the api
@router.get("/version")
def version():
    "Commit SHA of the deployed version"
    return {"version": environ.get("GIT_SHA", "unknown")}


# Return the healthcheck of the service
@router.get("/healthcheck")
def healthcheck():
    "Simple healthcheck to check if the service is running. Connects to the dynamoDB and sees if it can describe or main table"
    try:
        # connect and get the url_shortener table. After that, describe the table to make sure that it exists and there are no errors
        # associated with it. If there are errors, return an error message indicating the error
        client = boto3.client(
            "dynamodb",
            endpoint_url=(environ.get("DYNAMODB_HOST", None)),
            region_name="ca-central-1",
        )
        table_name = environ.get("TABLE_NAME", "url_shortener")
        client.describe_table(TableName=table_name)
    except botocore.exceptions.ClientError as err:
        return {
            "status": "ERROR",
            "message": f"Couldn't check for existence of {table_name}. Here's why: {err.response['Error']['Code']}: {err.response['Error']['Message']}",
        }
    # catch all other exceptions and return the error message
    except Exception as err:
        return {"status": "ERROR", "message": str(err)}
    return {"status": "OK"}
