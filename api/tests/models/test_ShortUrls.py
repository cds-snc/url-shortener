from models import ShortUrls

from unittest.mock import patch


def test_create_short_url():
    short_url = ShortUrls.create_short_url("https://www.canada.ca", "test")
    assert short_url == "test"


@patch("models.ShortUrls.client.put_item")
def test_create_short_url_with_existing_url(mock_put_item):
    mock_put_item.return_value = {"ResponseMetadata": {"HTTPStatusCode": 400}}
    short_url = ShortUrls.create_short_url("https://www.canada.ca", "test")
    assert short_url is None


def test_get_short_url():
    ShortUrls.create_short_url("https://www.canada.ca", "test")
    short_url = ShortUrls.get_short_url("test")
    assert short_url["original_url"]["S"] == "https://www.canada.ca"
