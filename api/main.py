from os import environ

from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.responses import PlainTextResponse
from mangum import Mangum
from pydantic import BaseSettings
from starlette.middleware.base import BaseHTTPMiddleware

from middleware.cloudfront import check_header
from routers import shortener, ops


class Settings(BaseSettings):
    openapi_url: str = environ.get("OPENAPI_URL", "")


description = """
API to shorten a url
"""

ALLOWED_DOMAINS = environ.get("ALLOWED_DOMAINS", "").split(",")
SHORTENER_DOMAIN = environ.get("SHORTENER_DOMAIN", "")
DOCS_URL = environ.get("DOCS_URL", None)

if len(ALLOWED_DOMAINS) == 0:
    raise ValueError("ALLOWED_DOMAINS environment variable is empty")

if len(SHORTENER_DOMAIN.strip()) == 0:
    raise ValueError("SHORTENER_DOMAIN environment variable is empty")

# initialize the app with title, version and url
app = FastAPI(
    title="API shortener",
    description=description,
    version="0.0.1",
    docs_url=DOCS_URL,
    redoc_url=None,
)

# include other routes
app.include_router(ops.router)
app.include_router(shortener.router)

# include middleware
app.add_middleware(BaseHTTPMiddleware, dispatch=check_header)

# include the lambda handler function
handler = Mangum(app)

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
