import unittest
from models import ShortUrls
import time
import datetime
from unittest.mock import patch


class TestCreateShortUrl(unittest.TestCase):
    def test_create_short_url(self):
        short_url = ShortUrls.create_short_url("https://www.canada.ca", "test1234")
        assert short_url == "test1234"

    def test_create_short_url_with_existing_url__returns_same_shorten_url(self):
        url_a = ShortUrls.create_short_url("https://www.canada.ca", "test1234")
        url_b = ShortUrls.create_short_url("https://www.canada.ca", "test1234")
        assert url_a == url_b

    @patch("models.ShortUrls.client.put_item")
    def test_create_short_url_with_existing_url(self, mock_put_item):
        mock_put_item.return_value = {"ResponseMetadata": {"HTTPStatusCode": 400}}
        short_url = ShortUrls.create_short_url("https://www.canada.ca", "test")
        assert short_url is None

    def test_get_short_url(self):
        ShortUrls.create_short_url("https://www.canada.ca", "test")
        short_url = ShortUrls.get_short_url("test")
        assert short_url["original_url"]["S"] == "https://www.canada.ca"

    def test_ttl_is_valid(self):
        short_url = ShortUrls.get_short_url("test")
        epoch_time_now = int(time.time())
        assert int(short_url["ttl"]["N"]) > epoch_time_now

    def test_ttl_is_invalid(self):
        future_epoch_time = int(
            time.mktime(
                (
                    datetime.datetime.today() + datetime.timedelta(days=(365 * 5))
                ).timetuple()
            )
        )
        short_url = ShortUrls.get_short_url("test")
        assert short_url["ttl"]["N"] < str(future_epoch_time)

    def test_create_short_url_with_different_url_but_same_hash__raises_value_error_for_collision(
        self,
    ):
        with self.assertRaises(ValueError):
            ShortUrls.create_short_url("https://www.canada.ca", "test1234")
            ShortUrls.create_short_url("https://nrc.gc.ca", "test1234")
