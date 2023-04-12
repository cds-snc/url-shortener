import hashlib
import advocate
import os
import requests
import validators
import math
import base64
from urllib.parse import urlparse
from models import ShortUrls
from logger import log


def calculate_hash_bytes(length: int):
    """
    calculate_hash_bytes determines the number of bytes required for
    shake256 hashing algo given a desired output length.

    Base64 encodes three bytes to four characters. The calculation
    does not consider trimmed padding, if any exists.

    parameter length: desired output length
    returns: bytes required for shake 256 hashing
    """
    return math.ceil(3 * (length / 4))


def generate_short_url(
    original_url: str, pepper: str, length: int = 8, hint=None, padding=False
):
    """
    generate_short_url generates an length character hex digest used to
    represent the original url.

    parameter original_url: the url that the user passes to the api
    parameter pepper: secret to add to hashing
    parameter length: output length
    parameter hint: overrides output with specified value

    returns: base64 encoding, without padding, representing the shortened url
    """
    if hint:
        return hint

    length = max(length, 4)

    # note that the normal convention is to add pepper as a suffix
    data = original_url + pepper
    digest = hashlib.shake_256()
    digest.update(data.encode())

    return (
        base64.b64encode(digest.digest(calculate_hash_bytes(length)), altchars=b"AZ")
        .decode()
        .rstrip("=" if not padding else "")
    )


def is_domain_allowed(original_url):
    """is_domain_allowed determines if the domain of the url passed in as a parameter is allowed in a list of allowed domains
    parameter original_url: the url that the user passes to the api
    returns: True if the domain is allowed and False if it is not."""
    try:
        # Obtain the domain from the url
        domain = ".".join(urlparse(original_url).hostname.split(".")[-2:])
        return domain in os.getenv("ALLOWED_DOMAINS").split(",")
    except Exception:
        return {"error": "error retrieving domain"}


def is_valid_url(original_url):
    """is_valid_url determines if the url passed in as a parameter is a valid url
    parameter original_url: the url that the user passes to the api
    returns: True if the url is valid and False if it is not."""
    try:
        return validators.url(original_url)
    except Exception as err:
        log.error(f"Error in validating url: {original_url}: {err}")
        return False


def is_valid_scheme(original_url):
    """is_valid_scheme determines if scheme is https
    parameter original_url: the url that the user passes to the api
    returns: True if scheme is https, False otherwise"""
    return urlparse(original_url).scheme.casefold() == "https".casefold()


def resolve_short_url(short_url):
    """resolve_short_url function resolves the short url to the original url
    parameter short_url: the shortened url
    returns: the original url or False if the short url cannot be resolved"""
    if "CYPRESS_CI" in os.environ:
        return {"original_url": {"S": "https://digital.canada.ca/"}}
    result = ShortUrls.get_short_url(short_url)
    if result is None:
        log.error(f"Error in resolving url: {short_url}")
        return False
    return result


def return_short_url(original_url, peppers, created_by):
    """return_short_url function returns the shortened url
    parameter original_url: the url that the user passes to the api
    parameter peppers: peppers iterable used for hashing input
    returns: the shortened url or an error message if the shortened url cannot be generated
    """
    try:
        advocate.get(original_url)
    except advocate.UnacceptableAddressException:
        log.error(f"Unacceptable address: {original_url}")
        return {"error": "error_forbidden_resource"}
    except requests.RequestException as err:
        log.error(f"Failed to connect to {original_url}: {err}")
        return {"error": "error_filed_to_connect_url"}

    peppers_iter = iter(peppers)
    short_url = None

    while short_url is None:
        try:
            pepper = next(peppers_iter)
            try:
                candidate_url = generate_short_url(
                    original_url, pepper, int(os.getenv("SHORTENER_PATH_LENGTH"))
                )
                short_url = ShortUrls.create_short_url(
                    original_url, candidate_url, created_by
                )
            except ValueError as err:
                # collision
                log.info(
                    f"Retrying, collision detected for {candidate_url} "
                    f"generated for {original_url}: {err}"
                )
        except StopIteration:
            log.error("Could not generate URL, pepper(s) exhausted")
            return {"error": "error_url_shorten_failed"}

    return short_url


def validate_and_shorten_url(original_url, created_by):
    """validate_and_shorten_url function validates the url passed in as a parameter and then shortens it
    parameter original_url: the url that the user passes to the api
    returns: a dictionary containing the shortened url and the original url"""
    try:
        # Check to see if the url confronts to a valid format. If not then display error.
        if not is_valid_url(original_url):
            data = {
                "error": "Unable to shorten link. Invalid URL.",
                "original_url": original_url,
                "status": "ERROR",
            }
        # Else if scheme is invalid (i.e. not https), display error
        elif not is_valid_scheme(original_url):
            data = {
                "error": "error_url_shorten_invalid_scheme",
                "original_url": original_url,
                "status": "ERROR",
            }
        # Else if the domain is not allowed, display error and link to GC Forms page
        elif not is_domain_allowed(original_url):
            forms_url = os.getenv("FORMS_URL")
            data = {
                "error": "error_url_shorten_invalid_host",
                "form_url": forms_url,
                "original_url": original_url,
                "status": "ERROR",
            }
        # Else, we are all good to shorten!
        else:
            short_url = return_short_url(
                original_url, os.getenv("PEPPERS").split(","), created_by
            )

            if isinstance(short_url, dict):
                return {
                    "error": short_url["error"],
                    "original_url": original_url,
                    "status": "ERROR",
                }

            shortener_domain = os.getenv("SHORTENER_DOMAIN") or ""
            log.info(
                f"Shortened URL: '{short_url}' from '{original_url}' created by '{created_by}'"
            )
            data = {
                "short_url": f"{shortener_domain}{short_url}",
                "original_url": original_url,
                "status": "OK",
            }

    except Exception as err:
        data = {
            "error": f"Error in processing shortened url: {err}",
            "original_url": original_url,
            "status": "ERROR",
        }

    return data


def redact_value(value, min_length=8):
    """Given a value, redact it and display the last 4 characters of the value
    provided it is longer the minimum lenght (default 8)."""
    value_length = len(value)
    return (
        "*" * (value_length - 4) + value[-4:]
        if value_length >= min_length
        else "*" * value_length
    )
