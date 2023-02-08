import hashlib
import base64
import advocate
import os
import requests
import validators
from datetime import datetime, timezone
from urllib.parse import urlparse
from models import ShortUrls
from logger import log


def generate_short_url(original_url: str, timestamp: float, shortened_length: int = 8):
    """generate_short_url generates an shortened_length character string used to represent the original url. This shortened_length character
    string will be used to "unshorten" to the original url submitted.
    parameter original_url: the url that the user passes to the api
    parameter timestamp: the current datatime timestamp
    returns: an shortened_length character string representing the shortened url"""
    if shortened_length < 4:
        shortened_length = 4
    to_encode_str = f"{original_url}{timestamp}"
    b64_encoded_str = base64.urlsafe_b64encode(
        hashlib.sha256(to_encode_str.encode()).digest()
    ).decode()
    return b64_encoded_str[:shortened_length]


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
    except Exception:
        log.info(f"Error in validating url: {original_url}")
        return False


def resolve_short_url(short_url):
    """resolve_short_url function resolves the short url to the original url
    parameter short_url: the shortened url
    returns: the original url or False if the short url cannot be resolved"""
    result = ShortUrls.get_short_url(short_url)
    if result is None:
        log.info(f"Error in resolving url: {short_url}")
        return False
    return result


def return_short_url(original_url):
    """return_short_url function returns the shortened url
    parameter original_url: the url that the user passes to the api
    returns: the shortened url or an error message if the shortened url cannot be generated"""
    try:
        timestamp = datetime.now().replace(tzinfo=timezone.utc).timestamp()
        try:
            advocate.get(original_url)
        except advocate.UnacceptableAddressException:
            log.info(f"Unacceptable address: {original_url}")
            return {"error": "That URL points to a forbidden resource"}
        except requests.RequestException:
            log.info(f"Failed to connect: {original_url}")
            return {"error": "Failed to connect to the specified URL"}
        short_url = generate_short_url(original_url, timestamp)
        short_url_obj = ShortUrls.create_short_url(original_url, short_url)
        if not short_url_obj:
            log.info(f"Could not save URL: {original_url} | {short_url}")
            return {"error": "Error in processing shortened url"}
        return short_url
    except Exception as err:
        log.error(f"Error processing URL: {original_url} | {err}")
        return {"error": "Error in processing shortened url"}


def validate_and_shorten_url(original_url):
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
        # Else if the domain is not allowed, display error and link to GC Forms page
        elif not is_domain_allowed(original_url):
            forms_url = os.getenv("FORMS_URL")
            data = {
                "error": "URL is not registered in our system as an Official GC Domain.",
                "form_url": forms_url,
                "original_url": original_url,
                "status": "ERROR",
            }
        # Else, we are all good to shorten!
        else:
            short_url = return_short_url(original_url)

            if isinstance(short_url, dict):
                return {
                    "error": short_url["error"],
                    "original_url": original_url,
                    "status": "ERROR",
                }

            shortener_domain = os.getenv("SHORTENER_DOMAIN") or ""
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
