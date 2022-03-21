import hashlib
import base64
import advocate
import requests
import validators
from datetime import datetime, timezone
from urllib.parse import urlparse
from models.ShortUrls import ShortUrls
from models.AllowedDomains import AllowedDomains


# Function to generate the 8 character short url
def generate_short_url(original_url: str, timestamp: float):
	"""generate_short_url generates an 8 character string used to represent the original url. This 8 character
	string will be used to "unshorten" to the original url submitted.
	parameter original_url: the url that the user passes to the api
	parameter timestamp: the current datatime timestamp
	returns: an 8 character string representing the shortened url"""
	to_encode_str = f'{original_url}{timestamp}'
	b64_encoded_str = base64.urlsafe_b64encode(
		hashlib.sha256(to_encode_str.encode()).digest()).decode()
	return b64_encoded_str[:8]


# Function to return the shortened url
def return_short_url(original_url, db_session):
	try:
		timestamp = datetime.now().replace(tzinfo=timezone.utc).timestamp()
		try:
			resp = advocate.get(original_url)
		except advocate.UnacceptableAddressException:
			return {"error": "That URL points to a forbidden resource"}
		except requests.RequestException:
			return {"error": "Failed to connect to the specified URL"}
		short_url = generate_short_url(original_url, timestamp)
		short_url_obj = ShortUrls(
			original_url=original_url, short_url=short_url)
		db_session.add(short_url_obj)
		db_session.commit()
		return short_url
	except Exception as err:
		return {"error": f"error in processing shortened url"}


def is_domain_allowed(original_url, db_session):
	"""is_domain_allowed function determines if a passed in url is in the allowed list of government
	   domains. It queries the table allowed_domains to determine if the url is allowed to be shortened
	   parameter original_url: the url that the user passes to the api
	   parameter db_session: the database sesion
	   returns: True if the url contains a domain that is allowed or False if it does not
	   """
	try:
		# Obtain the domain from the url
		domain = urlparse(original_url).hostname
		# Query the table allowed_domains to see if the domain exists.
		domain_obj = db_session.query(AllowedDomains).filter(
			AllowedDomains.domain == domain).first()
		if domain_obj is not None:
			return True
		return False
	except Exception as err:
		return {"error": "error retrieving domain"}


def is_valid_url(original_url):
	"""is_valid_url determines if the url passed in as a parameter is a valid url
	parameter original_url: the url that the user passes to the api
	returns: True if the url is valid and False if it is not. """
	return validators.url(original_url)