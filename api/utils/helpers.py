import hashlib
import base64
import advocate
import os
import requests
import validators
from datetime import datetime, timezone
from urllib.parse import urlparse
from models.ShortUrls import ShortUrls
from models.AllowedDomains import AllowedDomains
from sqlalchemy.exc import SQLAlchemyError
from logger import log


def generate_short_url(original_url: str, timestamp: float):
    """generate_short_url generates an 8 character string used to represent the original url. This 8 character
    string will be used to "unshorten" to the original url submitted.
    parameter original_url: the url that the user passes to the api
    parameter timestamp: the current datatime timestamp
    returns: an 8 character string representing the shortened url"""
    to_encode_str = f"{original_url}{timestamp}"
    b64_encoded_str = base64.urlsafe_b64encode(
        hashlib.sha256(to_encode_str.encode()).digest()
    ).decode()
    return b64_encoded_str[:8]


def is_domain_allowed(original_url, db_session):
    """is_domain_allowed function determines if a passed in url is in the allowed list of government
    domains. It queries the table allowed_domains to determine if the url is allowed to be shortened
    parameter original_url: the url that the user passes to the api
    parameter db_session: the database sesion
    returns: True if the url contains a domain that is allowed or False if it does not
    """
    try:
        # Obtain the domain from the url
        domain = ".".join(urlparse(original_url).hostname.split(".")[-2:])
        # Query the table allowed_domains to see if the domain exists.
        domain_obj = (
            db_session.query(AllowedDomains)
            .filter(AllowedDomains.domain == domain)
            .first()
        )
        if domain_obj is not None:
            return True
        return False
    except Exception:
        return {"error": "error retrieving domain"}


def is_valid_url(original_url):
    """is_valid_url determines if the url passed in as a parameter is a valid url
    parameter original_url: the url that the user passes to the api
    returns: True if the url is valid and False if it is not."""
    try:
        return validators.url(original_url)
    except Exception:
        return False


def resolve_short_url(short_url, db_session):
    """resolve_short_url function resolves the short url to the original url
    parameter short_url: the shortened url
    parameter db_session: the database session
    returns: the original url or an error message if the short url does not exist"""
    try:
        short_url_obj = (
            db_session.query(ShortUrls).filter(ShortUrls.short_url == short_url).first()
        )
        if short_url_obj is None:
            return False
        return short_url_obj
    except SQLAlchemyError as err:
        log.error(err)
        return False


def return_short_url(original_url, db_session):
    """return_short_url function returns a shortened url if the original url is valid and allowed
    parameter original_url: the url that the user passes to the api
    parameter db_session: the database session
    returns: the shortened url or an error message if the short url cannot be generated"""
    try:
        timestamp = datetime.now().replace(tzinfo=timezone.utc).timestamp()
        try:
            advocate.get(original_url)
        except advocate.UnacceptableAddressException:
            return {"error": "That URL points to a forbidden resource"}
        except requests.RequestException:
            return {"error": "Failed to connect to the specified URL"}
        short_url = generate_short_url(original_url, timestamp)
        short_url_obj = ShortUrls(original_url=original_url, short_url=short_url)
        db_session.add(short_url_obj)
        db_session.commit()
        return short_url
    except Exception:
        return {"error": "Error in processing shortened url"}


def validate_and_shorten_url(original_url, db_session):
    """validate_and_shorten_url function validates the url passed in as a parameter and then shortens it
    parameter original_url: the url that the user passes to the api
    parameter db_session: the database session
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
        elif not is_domain_allowed(original_url, db_session):
            forms_url = os.getenv("FORMS_URL")
            data = {
                "error": "URL is not registered in our system as an Official GC Domain.",
                "form_url": forms_url,
                "original_url": original_url,
                "status": "ERROR",
            }
        # Else, we are all good to shorten!
        else:
            short_url = return_short_url(original_url, db_session)

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
