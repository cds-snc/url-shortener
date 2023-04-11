import pytest
from fastapi.exceptions import HTTPException
from unittest.mock import MagicMock, patch
from starlette.status import HTTP_401_UNAUTHORIZED
from utils import auth_token


@patch("utils.auth_token.VALID_AUTH_TOKENS", ["auth_token"])
def test_valid_token():
    mock_request = MagicMock()
    assert auth_token.validate_auth_token("auth_token", mock_request) == "auth_token"


def test_invalid_token():
    with pytest.raises(HTTPException) as http_exception:
        mock_request = MagicMock()
        auth_token.validate_auth_token("auth_token", mock_request)
    assert http_exception.value.status_code == HTTP_401_UNAUTHORIZED
    assert http_exception.value.headers == {
        "WWW-Authenticate": 'Bearer realm="UrlShortener", error="invalid_token", error_description="The api key is invalid"',
    }


def test_missing_token():
    with pytest.raises(HTTPException) as http_exception:
        mock_request = MagicMock()
        mock_request.headers = {}
        auth_token.validate_auth_token(None, mock_request)
    assert http_exception.value.status_code == HTTP_401_UNAUTHORIZED
    assert http_exception.value.headers == {
        "WWW-Authenticate": 'Bearer realm="UrlShortener"',
    }
