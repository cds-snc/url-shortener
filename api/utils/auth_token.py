import os
from typing import Annotated

from fastapi import Depends
from fastapi.exceptions import HTTPException
from fastapi.security import OAuth2PasswordBearer
from starlette.requests import Request
from starlette.status import HTTP_401_UNAUTHORIZED

from logger import log

AUTH_TOKEN_APP = os.environ.get("AUTH_TOKEN_APP", None)
AUTH_TOKEN_NOTIFY = os.environ.get("AUTH_TOKEN_NOTIFY", None)
VALID_AUTH_TOKENS = [AUTH_TOKEN_APP, AUTH_TOKEN_NOTIFY]

if not AUTH_TOKEN_APP:
    raise ValueError("AUTH_TOKEN_APP environment variable is empty")

if not AUTH_TOKEN_NOTIFY:
    raise ValueError("AUTH_TOKEN_NOTIFY environment variable is empty")


# We are using OAuth2PasswordBearer to validate static bearer tokens
# without a way for a user to self-serve generate JWTs. This can be enhanced
# generate and validate JWT tokens once we have an identity provider.
oauth2_bearer = OAuth2PasswordBearer(tokenUrl="", auto_error=False)


def validate_auth_token(
    token: Annotated[str, Depends(oauth2_bearer)], request: Request
) -> str | None:
    """
    Validate that a request has an Authorization header with a valid bearer token.
    """
    is_valid = isinstance(token, str) and token.strip() and token in VALID_AUTH_TOKENS
    if not is_valid:
        log.warning(
            "SUSPICIOUS: unable to validate auth token for an authenticated route"
        )
        authorization = request.headers.get("Authorization")
        error_attributes = (
            ', error="invalid_token", error_description="The api key is invalid"'
            if authorization
            else ""
        )
        raise HTTPException(
            status_code=HTTP_401_UNAUTHORIZED,
            headers={
                "WWW-Authenticate": 'Bearer realm="UrlShortener"' + error_attributes,
            },
        )
    return token
