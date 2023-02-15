from fastapi import FastAPI
from os import environ
from pydantic import BaseSettings
from routers import shortener, ops
from fastapi.staticfiles import StaticFiles
from fastapi.responses import PlainTextResponse

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
app.include_router(ops.router)
app.include_router(shortener.router)

# Mount static directory
app.mount("/static", StaticFiles(directory="static"), name="static")

# Response for /.well-known/security.txt
app.get("/.well-known/security.txt", response_class=PlainTextResponse)(
    lambda: """Contact: mailto:security-securite@cds-snc.ca
Preferred-Languages: en, fr
Policy: https://digital.canada.ca/legal/security-notice
Hiring: https://digital.canada.ca/join-our-team/
Hiring: https://numerique.canada.ca/rejoindre-notre-equipe/
"""
)
