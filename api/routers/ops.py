"""
API routes for for operational and status requests
"""
from os import environ
from fastapi import APIRouter


router = APIRouter()


# Return the current version of the api
@router.get("/version")
def version():
    "Commit SHA of the deployed version"
    return {"version": environ.get("GIT_SHA", "unknown")}
