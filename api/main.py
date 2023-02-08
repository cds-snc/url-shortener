from fastapi import FastAPI
from os import environ
from pydantic import BaseSettings
from routers import shortener
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles

from dotenv import load_dotenv

load_dotenv()


class Settings(BaseSettings):
    openapi_url: str = environ.get("OPENAPI_URL", "")


description = """
API to shorten a url
"""

allowed_domains = environ.get("ALLOWED_DOMAINS", "").split(",")
shortener_domain = environ.get("SHORTENER_DOMAIN", "")

if len(allowed_domains) == 0:
    raise ValueError("ALLOWED_DOMAINS environment variable is empty")

if shortener_domain.strip() == "":
    raise ValueError("SHORTENER_DOMAIN environment variable is empty")

# initialize the app with title, version and url
app = FastAPI(
    title="API shortener",
    description=description,
    version="0.0.1",
)

# include other routes
app.include_router(shortener.router)

templates = Jinja2Templates(directory="templates")

# Mount static directory
app.mount("/static", StaticFiles(directory="static"), name="static")
