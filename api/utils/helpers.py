import hashlib
import base64

def generate_short_url(original_url: str, timestamp: float):
	to_encode_str = f'{original_url}{timestamp}'

	b64_encoded_str = base64.urlsafe_b64encode(
		hashlib.sha256(to_encode_str.encode()).digest()).decode()
	return b64_encode_str[:8]
