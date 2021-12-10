from fastapi import FastAPI
from os import environ
from pydantic import BaseSettings
from routers import shortener

class Settings(BaseSettings):
	openapi_url: str = environ.get("OPENAPI_URL", "")

description = """ 
API to shorten a url
"""

# initialize the app with title, version and url
app = FastAPI(
	title="API shortener",
	description= description,
	version="0.0.1",
	#openapi_url=settings.openapi_url,
)

# include other routes
app.include_router(shortener.router)
