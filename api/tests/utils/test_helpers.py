import datetime
import os
import random
import string

from unittest.mock import MagicMock, patch

import advocate
import jwt
import requests

from utils import helpers


def round_to(n, roundto):
    return (n + (roundto - 1)) & ~(roundto - 1)


def test_calculate_hash_bytes_ok():
    for length, b in [(4, 3), (5, 4), (6, 5), (7, 6), (8, 6), (9, 7), (10, 8)]:
        assert helpers.calculate_hash_bytes(length) == b


def test_translate_safe_charset__letters_translated_ok():
    safe_charset = "AAEEEFHHJJKLQQQQQRSSWWWXYZaaedefhhhjklqqqqqrsswwwxyz2224456789AZ"
    tr = "".join(random.choice(string.ascii_letters + "+/") for i in range(100))
    assert all(c in safe_charset for c in helpers.translate_safe_charset(tr))


def test_translate_safe_charset__digits_translated_ok():
    safe_charset = "AAEEEFHHJJKLQQQQQRSSWWWXYZaaedefhhhjklqqqqqrsswwwxyz2224456789AZ"
    tr = "".join(random.choice(string.digits) for i in range(100))
    assert all(c in safe_charset for c in helpers.translate_safe_charset(tr))


def test_generate_short_url__length_ok():
    original_url = "https://example.com"
    pepper = "T4XuCG/uaDY7uHG+hG/01OOdgO77bl4GOdY5foLEHb8="
    for n in range(4, 11):
        assert len(
            helpers.generate_short_url(original_url, pepper, n, padding=True)
        ) == round_to(n, 4)


def test_generate_short_url__no_padding():
    original_url = "https://example.com"
    pepper = "T4XuCG/uaDY7uHG+hG/01OOdgO77bl4GOdY5foLEHb8="
    for n in range(4, 11):
        assert "=" not in helpers.generate_short_url(original_url, pepper, n)


def test_generate_short_url__hash_is_same():
    original_url = "https://example.com"
    pepper = "T4XuCG/uaDY7uHG+hG/01OOdgO77bl4GOdY5foLEHb8="
    url_a = helpers.generate_short_url(original_url, pepper)
    url_b = helpers.generate_short_url(original_url, pepper)
    assert url_a == url_b


def test_generate_short_url__min_length_equals_4_digits():
    original_url = "https://example.com"
    pepper = "T4XuCG/uaDY7uHG+hG/01OOdgO77bl4GOdY5foLEHb8="
    short_url = helpers.generate_short_url(original_url, pepper, 1)
    assert len(short_url) == 4


def test_generate_short_url__hint_passed():
    original_url = "https://example.com"
    pepper = "T4XuCG/uaDY7uHG+hG/01OOdgO77bl4GOdY5foLEHb8="
    short_url = helpers.generate_short_url(original_url, pepper, hint="FizzBuzz")
    assert short_url == "FizzBuzz"


@patch("utils.helpers.ShortUrls")
@patch("utils.helpers.generate_short_url")
@patch("utils.helpers.advocate")
def test_return_short_url_succeeds_if_advocate_passes(
    mock_advocate, mock_generate_short_url, mock_short_urls_model
):
    original_url = "https://example.com"
    mock_advocate.get.return_value = True
    mock_short_urls_model.create_short_url.return_value = "FizzBuzz"
    mock_generate_short_url.return_value = "FizzBuzz"
    peppers = [
        "T4XuCG/uaDY7uHG+hG/01OOdgO77bl4GOdY5foLEHb8=",
        "dPG6wEcrcOYc6lxqC/Hv3QD7CAHkzZ1wA0gZQW1kvkY=",
    ]
    short_url = helpers.return_short_url(original_url, peppers, "actor")
    assert short_url == "FizzBuzz"


@patch("utils.helpers.ShortUrls")
@patch("utils.helpers.generate_short_url")
@patch("utils.helpers.advocate")
def test_return_short_url_succeeds_if_advocate_passes_but_save_fails(
    mock_advocate, mock_generate_short_url, mock_short_urls_model
):
    original_url = "https://example.com"
    mock_advocate.get.return_value = True
    mock_short_urls_model.create_short_url.return_value = None
    mock_generate_short_url.return_value = "FizzBuzz"
    peppers = [
        "T4XuCG/uaDY7uHG+hG/01OOdgO77bl4GOdY5foLEHb8=",
        "dPG6wEcrcOYc6lxqC/Hv3QD7CAHkzZ1wA0gZQW1kvkY=",
    ]
    result = helpers.return_short_url(original_url, peppers, "actor")
    assert result == {"error": "error_url_shorten_failed"}


def test_return_short_url_unacceptable_address_exception():
    original_url = "https://example.com"
    advocate.get = MagicMock(side_effect=advocate.UnacceptableAddressException)
    peppers = [
        "T4XuCG/uaDY7uHG+hG/01OOdgO77bl4GOdY5foLEHb8=",
        "dPG6wEcrcOYc6lxqC/Hv3QD7CAHkzZ1wA0gZQW1kvkY=",
    ]
    result = helpers.return_short_url(original_url, peppers, "actor")
    assert result == {"error": "error_forbidden_resource"}


def test_return_short_url_request_exception():
    original_url = "https://example.com"
    advocate.get = MagicMock(side_effect=requests.RequestException)
    peppers = [
        "T4XuCG/uaDY7uHG+hG/01OOdgO77bl4GOdY5foLEHb8=",
        "dPG6wEcrcOYc6lxqC/Hv3QD7CAHkzZ1wA0gZQW1kvkY=",
    ]
    result = helpers.return_short_url(original_url, peppers, "actor")
    assert result == {"error": "error_filed_to_connect_url"}


def test_is_domain_allowed_returns_true_if_it_exists():
    original_url = "https://canada.ca"
    result = helpers.is_domain_allowed(original_url)
    assert result is True


def test_is_domain_allowed_returns_false_if_it_does_not_exist():
    original_url = "https://example.com"
    result = helpers.is_domain_allowed(original_url)
    assert result is False


@patch("utils.helpers.urlparse")
def test_is_domain_allowed_returns_exception(mock_urlparse):
    original_url = "https://example.com"
    mock_urlparse.side_effect = Exception
    result = helpers.is_domain_allowed(original_url)
    assert result == {"error": "error retrieving domain"}


def test_is_valid_url_returns_true_if_valid():
    original_url = "http://example.com"
    result = helpers.is_valid_url(original_url)
    assert result is True


@patch("utils.helpers.validators")
def test_is_valid_url_returns_false_if_throws_an_exception(mock_validators):
    original_url = "https://example.com"
    mock_validators.url.side_effect = Exception
    result = helpers.is_valid_url(original_url)
    assert result is False


@patch("utils.helpers.ShortUrls")
@patch.dict(os.environ, {"ALLOWED_DOMAINS": "foo_bar.com"}, clear=True)
def test_resolve_short_url_returns_original_url(mock_short_urls_model):
    short_url = "XjbS35ah"
    mock_short_urls_model.get_short_url.return_value = {
        "original_url": {"S": "https://foo_bar.com"},
    }
    result = helpers.resolve_short_url(short_url)
    assert result == {
        "original_url": {"S": "https://foo_bar.com"},
    }


@patch("utils.helpers.ShortUrls")
def test_resolve_short_url_returns_false_if_it_does_not_exist(mock_short_urls_model):
    short_url = "XjbS35ah"
    mock_short_urls_model.get_short_url.return_value = None
    result = helpers.resolve_short_url(short_url)
    assert result is False


@patch("utils.helpers.ShortUrls")
@patch.dict(os.environ, {"ALLOWED_DOMAINS": "bam_baz.com"}, clear=True)
def test_resolve_short_url_returns_false_if_it_is_not_allowed(mock_short_urls_model):
    short_url = "XjbS35ah"
    mock_short_urls_model.get_short_url.return_value = {
        "original_url": {"S": "https://foo_bar.com"},
    }
    result = helpers.resolve_short_url(short_url)
    assert result is False


@patch.dict(os.environ, {"CYPRESS_CI": "1"}, clear=True)
def test_resolve_short_url_returns_fixture_if_cypress_env_var_is_set():
    short_url = "XjbS35ah"
    result = helpers.resolve_short_url(short_url)
    assert result == {"original_url": {"S": "https://digital.canada.ca/"}}


def test_validate_and_shorten_url_returns_error_if_invalid_url():
    original_url = "https://example.com"
    helpers.is_valid_url = MagicMock(return_value=False)
    result = helpers.validate_and_shorten_url(original_url, "actor")
    assert result == {
        "error": "error_url_shorten_url_not_valid",
        "original_url": original_url,
        "status": "ERROR",
    }


def test_validate_and_shorten_url_returns_error_if_domain_not_allowed():
    original_url = "https://example.com"
    helpers.is_valid_url = MagicMock(return_value=True)
    helpers.is_domain_allowed = MagicMock(return_value=False)
    result = helpers.validate_and_shorten_url(original_url, "actor")
    assert result == {
        "error": "error_url_shorten_invalid_host",
        "original_url": original_url,
        "status": "ERROR",
    }


def test_validate_and_shorten_url_returns_error_if_return_short_url_exception():
    original_url = "https://example.com"
    helpers.is_valid_url = MagicMock(return_value=True)
    helpers.is_domain_allowed = MagicMock(return_value=True)
    helpers.return_short_url = MagicMock(
        return_value={"error": "That URL points to a forbidden resource"}
    )
    result = helpers.validate_and_shorten_url(original_url, "actor")
    assert result == {
        "error": "That URL points to a forbidden resource",
        "original_url": original_url,
        "status": "ERROR",
    }


def test_validate_and_shorten_url_returns_error_if_any_type_of_exception():
    original_url = "https://example.com"
    helpers.is_valid_url.side_effect = Exception("FAILED")
    result = helpers.validate_and_shorten_url(original_url, "actor")
    assert result == {
        "error": "error_url_shorten_failed",
        "original_url": original_url,
        "status": "ERROR",
    }


@patch.dict(os.environ, {"SHORTENER_DOMAIN": "http://127.0.0.1:8000/"})
def test_validate_and_shorten_url_returns_success():
    original_url = "https://example.com"
    peppers = [
        "T4XuCG/uaDY7uHG+hG/01OOdgO77bl4GOdY5foLEHb8=",
        "dPG6wEcrcOYc6lxqC/Hv3QD7CAHkzZ1wA0gZQW1kvkY=",
    ]
    helpers.is_valid_url = MagicMock(return_value=True)
    helpers.is_domain_allowed = MagicMock(return_value=True)
    helpers.return_short_url = MagicMock(return_value="XjbS35ah")
    result = helpers.validate_and_shorten_url(original_url, "actor")
    assert result == {
        "original_url": original_url,
        "short_url": "http://127.0.0.1:8000/XjbS35ah",
        "status": "OK",
    }
    helpers.return_short_url.assert_called_once_with(original_url, peppers, "actor")


@patch.dict(os.environ, {"SHORTENER_DOMAIN": "https://foo.bar/"})
def test_validate_and_shorten_url_returns_success_with_domain():
    original_url = "https://example.com"
    peppers = [
        "T4XuCG/uaDY7uHG+hG/01OOdgO77bl4GOdY5foLEHb8=",
        "dPG6wEcrcOYc6lxqC/Hv3QD7CAHkzZ1wA0gZQW1kvkY=",
    ]
    helpers.is_valid_url = MagicMock(return_value=True)
    helpers.is_domain_allowed = MagicMock(return_value=True)
    helpers.return_short_url = MagicMock(return_value="XjbS35ah")
    result = helpers.validate_and_shorten_url(original_url, "anotheractor")
    assert result == {
        "original_url": original_url,
        "short_url": "https://foo.bar/XjbS35ah",
        "status": "OK",
    }
    helpers.return_short_url.assert_called_once_with(
        original_url, peppers, "anotheractor"
    )


def test_is_valid_scheme_https():
    assert helpers.is_valid_scheme("https://example.com")
    assert not helpers.is_valid_scheme("http://example.com")
    assert not helpers.is_valid_scheme("ftp://example.com")
    assert not helpers.is_valid_scheme("file://example.com")


def test_redact_value():
    assert helpers.redact_value("foo") == "***"
    assert helpers.redact_value("foobar", 1) == "**obar"
    assert helpers.redact_value("foobarbam") == "*****rbam"


@patch("utils.helpers.NotificationsAPIClient")
def test_notification_client(mock_notifications_api_client):
    assert helpers.notification_client() == mock_notifications_api_client.return_value


@patch("utils.helpers.datetime")
@patch("utils.helpers.jwt")
def test_generate_token(mock_jwt, mock_datetime):
    mock_datetime.datetime.utcnow.return_value = datetime.datetime(1970, 1, 1, 0, 0, 0)
    mock_datetime.timedelta.return_value = datetime.timedelta(minutes=1)
    helpers.generate_token("foo")
    mock_jwt.encode.assert_called_once_with(
        {"exp": datetime.datetime(1970, 1, 1, 0, 1)},
        key="foo",
        algorithm="HS256",
    )


def test_validate_token_is_valid():
    token = jwt.encode(
        {"exp": datetime.datetime.utcnow() + datetime.timedelta(minutes=1)},
        key="foo",
        algorithm="HS256",
    )
    assert helpers.validate_token(token, "foo") is True


def test_validate_token_is_not_valid():
    token_bad_sig = jwt.encode(
        {"exp": datetime.datetime.utcnow() + datetime.timedelta(minutes=1)},
        key="foo",
        algorithm="HS256",
    )
    assert helpers.validate_token(token_bad_sig, "bar") is False

    token_expired = jwt.encode(
        {"exp": datetime.datetime.utcnow() + datetime.timedelta(minutes=-1)},
        key="foo",
        algorithm="HS256",
    )
    assert helpers.validate_token(token_expired, "foo") is False

    assert helpers.validate_token("", "foo") is False
    assert helpers.validate_token(None, "foo") is False
