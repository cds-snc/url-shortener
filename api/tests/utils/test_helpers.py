from utils import helpers

from unittest.mock import MagicMock, patch

import advocate
import requests
import os


def test_generate_short_url():
    original_url = "http://example.com"
    timestamp = 123456789
    short_url = helpers.generate_short_url(original_url, timestamp)
    assert len(short_url) == 8
    assert short_url == "XjbS35ah"


def test_generate_short_url_with_short_string():
    original_url = "http://example.com"
    timestamp = 123456789
    short_url = helpers.generate_short_url(original_url, timestamp, 3)
    assert len(short_url) == 4
    assert short_url == "XjbS"


@patch("utils.helpers.ShortUrls")
@patch("utils.helpers.generate_short_url")
@patch("utils.helpers.advocate")
def test_return_short_url_succeeds_if_advoacte_passes(
    mock_advocate, mock_generate_short_url, mock_short_urls_model
):
    original_url = "http://example.com"
    mock_advocate.get.return_value = True
    mock_short_urls_model.create_short_url.return_value = True
    mock_generate_short_url.return_value = "FizzBuzz"
    short_url = helpers.return_short_url(original_url)
    assert len(short_url) == 8
    assert short_url == "FizzBuzz"


@patch("utils.helpers.ShortUrls")
@patch("utils.helpers.generate_short_url")
@patch("utils.helpers.advocate")
def test_return_short_url_succeeds_if_advoacte_passes_but_save_fails(
    mock_advocate, mock_generate_short_url, mock_short_urls_model
):
    original_url = "http://example.com"
    mock_advocate.get.return_value = True
    mock_short_urls_model.create_short_url.return_value = None
    mock_generate_short_url.return_value = "FizzBuzz"
    result = helpers.return_short_url(original_url)
    assert result == {"error": "Error in processing shortened url"}


def test_return_short_url_unacceptable_address_exception():
    original_url = "http://example.com"
    advocate.get = MagicMock(side_effect=advocate.UnacceptableAddressException)
    result = helpers.return_short_url(original_url)
    assert result == {"error": "That URL points to a forbidden resource"}


def test_return_short_url_request_exception():
    original_url = "http://example.com"
    advocate.get = MagicMock(side_effect=requests.RequestException)
    result = helpers.return_short_url(original_url)
    assert result == {"error": "Failed to connect to the specified URL"}


def test_return_short_url_exception():
    original_url = "http://example.com"
    advocate.get = MagicMock(side_effect=Exception)
    result = helpers.return_short_url(original_url)
    assert result == {"error": "Error in processing shortened url"}


@patch("utils.helpers.ShortUrls")
@patch("utils.helpers.advocate")
def test_return_short_url_ShortUrls_model_exception(
    mock_advocate, mock_short_urls_model
):
    original_url = "http://example.com"
    mock_advocate.get.return_value = True
    mock_short_urls_model.create_short_url.side_effect = Exception
    result = helpers.return_short_url(original_url)
    assert result == {"error": "Error in processing shortened url"}


def test_is_domain_allowed_returns_true_if_it_exists():
    original_url = "http://canada.ca"
    result = helpers.is_domain_allowed(original_url)
    assert result is True


def test_is_domain_allowed_returns_false_if_it_does_not_exist():
    original_url = "http://example.com"
    result = helpers.is_domain_allowed(original_url)
    assert result is False


@patch("utils.helpers.urlparse")
def test_is_domain_allowed_returns_exception(mock_urlparse):
    original_url = "http://example.com"
    mock_urlparse.side_effect = Exception
    result = helpers.is_domain_allowed(original_url)
    assert result == {"error": "error retrieving domain"}


def test_is_valid_url_returns_true_if_valid():
    original_url = "http://example.com"
    result = helpers.is_valid_url(original_url)
    assert result is True


@patch("utils.helpers.validators")
def test_is_valid_url_returns_false_if_throws_an_exception(mock_validators):
    original_url = "http://example.com"
    mock_validators.url.side_effect = Exception
    result = helpers.is_valid_url(original_url)
    assert result is False


@patch("utils.helpers.ShortUrls")
def test_resolve_short_url_returns_original_url(mock_short_urls_model):
    short_url = "XjbS35ah"
    mock_short_urls_model.get_short_url.return_value = "http://example.com"
    result = helpers.resolve_short_url(short_url)
    assert result == "http://example.com"


@patch("utils.helpers.ShortUrls")
def test_resolve_short_url_returns_false_if_it_does_not_exist(mock_short_urls_model):
    short_url = "XjbS35ah"
    mock_short_urls_model.get_short_url.return_value = None
    result = helpers.resolve_short_url(short_url)
    assert result is False


def test_validate_and_shorten_url_returns_error_if_invalid_url():
    original_url = "http://example.com"
    helpers.is_valid_url = MagicMock(return_value=False)
    result = helpers.validate_and_shorten_url(original_url)
    assert result == {
        "error": "Unable to shorten link. Invalid URL.",
        "original_url": original_url,
        "status": "ERROR",
    }


@patch.dict(os.environ, {"FORMS_URL": "foo"}, clear=True)
def test_validate_and_shorten_url_returns_error_if_domain_not_allowed():
    original_url = "http://example.com"
    helpers.is_valid_url = MagicMock(return_value=True)
    helpers.is_domain_allowed = MagicMock(return_value=False)
    result = helpers.validate_and_shorten_url(original_url)
    assert result == {
        "error": "URL is not registered in our system as an Official GC Domain.",
        "form_url": "foo",
        "original_url": original_url,
        "status": "ERROR",
    }


def test_validate_and_shorten_url_returns_error_if_return_short_url_exception():
    original_url = "http://example.com"
    helpers.is_valid_url = MagicMock(return_value=True)
    helpers.is_domain_allowed = MagicMock(return_value=True)
    helpers.return_short_url = MagicMock(
        return_value={"error": "That URL points to a forbidden resource"}
    )
    result = helpers.validate_and_shorten_url(original_url)
    assert result == {
        "error": "That URL points to a forbidden resource",
        "original_url": original_url,
        "status": "ERROR",
    }


def test_validate_and_shorten_url_returns_error_if_any_type_of_exception():
    original_url = "http://example.com"
    helpers.is_valid_url.side_effect = Exception("FAILED")
    result = helpers.validate_and_shorten_url(original_url)
    assert result == {
        "error": "Error in processing shortened url: FAILED",
        "original_url": original_url,
        "status": "ERROR",
    }


def test_validate_and_shorten_url_returns_success():
    original_url = "http://example.com"
    helpers.is_valid_url = MagicMock(return_value=True)
    helpers.is_domain_allowed = MagicMock(return_value=True)
    helpers.return_short_url = MagicMock(return_value="XjbS35ah")
    result = helpers.validate_and_shorten_url(original_url)
    assert result == {
        "original_url": original_url,
        "short_url": "http://127.0.0.1:8000/XjbS35ah",
        "status": "OK",
    }


@patch.dict(os.environ, {"SHORTENER_DOMAIN": "https://foo.bar/"}, clear=True)
def test_validate_and_shorten_url_returns_success_with_domain():
    original_url = "http://example.com"
    helpers.is_valid_url = MagicMock(return_value=True)
    helpers.is_domain_allowed = MagicMock(return_value=True)
    helpers.return_short_url = MagicMock(return_value="XjbS35ah")
    result = helpers.validate_and_shorten_url(original_url)
    assert result == {
        "original_url": original_url,
        "short_url": "https://foo.bar/XjbS35ah",
        "status": "OK",
    }
