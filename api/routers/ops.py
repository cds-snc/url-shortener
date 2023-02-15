"""
API routes for for operational and status requests
"""
from os import environ
from fastapi import APIRouter
import boto3
from logger import log




router = APIRouter()




# Return the current version of the api
@router.get("/version")
def version():
   "Commit SHA of the deployed version"
   return {"version": environ.get("GIT_SHA", "unknown")}




# Return the healthcheck of the service
@router.get("/healthcheck")
def healthcheck():
   "Simple healthcheck to check if the service is running. Connects to the dynamoDB and sees if it can describe the main table"
   if is_db_up():
       return {"status": "OK", "message": "Able to connect to the database"}
   else:
       return {"status": "ERROR", "message": "Not able to connect to the database"}




# Get the status of the dynamoDB database. We create the datatabse with the specified table name and then describe the table, essentially checking its status.
def is_db_up():
   try:
       # connect and get the url_shortener table. After that, describe the table to make sure that it exists and there are no errors
       # associated with it. If there are errors, return False otherwise return True
       client = boto3.client(
           "dynamodb",
           endpoint_url=(environ.get("DYNAMODB_HOST", None)),
           region_name="ca-central-1",
       )
       table_name = environ.get("TABLE_NAME", "url_shortener")
       client.describe_table(TableName=table_name)
   # Catch all errors, log the error and return False
   except Exception as err:
       log.error(f"Error in healthcheck: {err}")
       return False
   return True

