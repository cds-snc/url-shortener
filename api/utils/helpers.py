import hashlib
import base64
import advocate
import requests
from datetime import datetime, timezone
from models.ShortUrls import ShortUrls

# Function to generate the 8 character short url
def generate_short_url(original_url: str, timestamp: float):
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
			original_url = original_url, short_url = short_url)
		db_session.add(short_url_obj)
		db_session.commit()
		return short_url
	except Exception as err:
		return{"error": f"error in processing shortened url"}