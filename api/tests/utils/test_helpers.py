from utils import helpers

from unittest.mock import MagicMock, Mock, patch

import advocate
import requests
import os
from sqlalchemy.exc import SQLAlchemyError


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


@patch("utils.helpers.generate_short_url")
@patch("utils.helpers.advocate")
def test_return_short_url_succeeds_if_advoacte_passes(
    mock_advocate, mock_generate_short_url
):
    original_url = "http://example.com"
    db_session = MagicMock()
    mock_advocate.get.return_value = True
    mock_generate_short_url.return_value = "FizzBuzz"
    short_url = helpers.return_short_url(original_url, db_session)
    assert len(short_url) == 8
    assert short_url == "FizzBuzz"
    db_session.add.assert_called_once()
    db_session.commit.assert_called_once()


def test_return_short_url_unacceptable_address_exception():
    original_url = "http://example.com"
    db_session = Mock()
    advocate.get = MagicMock(side_effect=advocate.UnacceptableAddressException)
    result = helpers.return_short_url(original_url, db_session)
    assert result == {"error": "That URL points to a forbidden resource"}
    db_session.add.assert_not_called()
    db_session.commit.assert_not_called()


def test_return_short_url_request_exception():
    original_url = "http://example.com"
    db_session = Mock()
    advocate.get = MagicMock(side_effect=requests.RequestException)
    result = helpers.return_short_url(original_url, db_session)
    assert result == {"error": "Failed to connect to the specified URL"}
    db_session.add.assert_not_called()
    db_session.commit.assert_not_called()


def test_return_short_url_exception():
    original_url = "http://example.com"
    db_session = Mock()
    advocate.get = MagicMock(side_effect=Exception)
    result = helpers.return_short_url(original_url, db_session)
    assert result == {"error": "Error in processing shortened url"}
    db_session.add.assert_not_called()
    db_session.commit.assert_not_called()


def test_is_domain_allowed_returns_true_if_it_exists():
    original_url = "http://example.com"
    db_session = Mock()
    db_session.query.return_value.filter.return_value.first.return_value = True
    result = helpers.is_domain_allowed(original_url, db_session)
    assert result is True


def test_is_domain_allowed_returns_false_if_it_does_not_exist():
    original_url = "http://example.com"
    db_session = Mock()
    db_session.query.return_value.filter.return_value.first.return_value = None
    result = helpers.is_domain_allowed(original_url, db_session)
    assert result is False


def test_is_domain_allowed_returns_exception():
    original_url = "http://example.com"
    db_session = Mock()
    db_session.query.return_value.filter.return_value.first.side_effect = Exception
    result = helpers.is_domain_allowed(original_url, db_session)
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


def test_resolve_short_url_returns_original_url():
    short_url = "XjbS35ah"
    db_session = Mock()
    db_session.query.return_value.filter.return_value.first.return_value = True
    result = helpers.resolve_short_url(short_url, db_session)
    assert result is True


def test_resolve_short_url_returns_false_if_it_does_not_exist():
    short_url = "XjbS35ah"
    db_session = Mock()
    db_session.query.return_value.filter.return_value.first.return_value = None
    result = helpers.resolve_short_url(short_url, db_session)
    assert result is False


def test_resolve_short_url_returns_exception():
    short_url = "XjbS35ah"
    db_session = Mock()
    db_session.query.return_value.filter.return_value.first.side_effect = (
        SQLAlchemyError
    )
    result = helpers.resolve_short_url(short_url, db_session)
    assert result is False


def test_validate_and_shorten_url_returns_error_if_invalid_url():
    original_url = "http://example.com"
    db_session = Mock()
    helpers.is_valid_url = MagicMock(return_value=False)
    result = helpers.validate_and_shorten_url(original_url, db_session)
    assert result == {
        "error": "Unable to shorten link. Invalid URL.",
        "original_url": original_url,
        "status": "ERROR",
    }


@patch.dict(os.environ, {"FORMS_URL": "foo"}, clear=True)
def test_validate_and_shorten_url_returns_error_if_domain_not_allowed():
    original_url = "http://example.com"
    db_session = Mock()
    helpers.is_valid_url = MagicMock(return_value=True)
    helpers.is_domain_allowed = MagicMock(return_value=False)
    result = helpers.validate_and_shorten_url(original_url, db_session)
    assert result == {
        "error": "URL is not registered in our system as an Official GC Domain.",
        "form_url": "foo",
        "original_url": original_url,
        "status": "ERROR",
    }


def test_validate_and_shorten_url_returns_error_if_return_short_url_exception():
    original_url = "http://example.com"
    db_session = Mock()
    helpers.is_valid_url = MagicMock(return_value=True)
    helpers.is_domain_allowed = MagicMock(return_value=True)
    helpers.return_short_url = MagicMock(
        return_value={"error": "That URL points to a forbidden resource"}
    )
    result = helpers.validate_and_shorten_url(original_url, db_session)
    assert result == {
        "error": "That URL points to a forbidden resource",
        "original_url": original_url,
        "status": "ERROR",
    }


def test_validate_and_shorten_url_returns_error_if_any_type_of_exception():
    original_url = "http://example.com"
    db_session = Mock()
    helpers.is_valid_url.side_effect = Exception("FAILED")
    result = helpers.validate_and_shorten_url(original_url, db_session)
    assert result == {
        "error": "Error in processing shortened url: FAILED",
        "original_url": original_url,
        "status": "ERROR",
    }


def test_validate_and_shorten_url_returns_success():
    original_url = "http://example.com"
    db_session = Mock()
    helpers.is_valid_url = MagicMock(return_value=True)
    helpers.is_domain_allowed = MagicMock(return_value=True)
    helpers.return_short_url = MagicMock(return_value="XjbS35ah")
    result = helpers.validate_and_shorten_url(original_url, db_session)
    assert result == {
        "original_url": original_url,
        "short_url": "XjbS35ah",
        "status": "OK",
    }


@patch.dict(os.environ, {"SHORTENER_DOMAIN": "https://foo.bar/"}, clear=True)
def test_validate_and_shorten_url_returns_success_with_domain():
    original_url = "http://example.com"
    db_session = Mock()
    helpers.is_valid_url = MagicMock(return_value=True)
    helpers.is_domain_allowed = MagicMock(return_value=True)
    helpers.return_short_url = MagicMock(return_value="XjbS35ah")
    result = helpers.validate_and_shorten_url(original_url, db_session)
    assert result == {
        "original_url": original_url,
        "short_url": "https://foo.bar/XjbS35ah",
        "status": "OK",
    }
