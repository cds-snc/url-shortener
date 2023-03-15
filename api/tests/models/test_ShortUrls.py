import unittest
from models import ShortUrls


class TestCreateShortUrl(unittest.TestCase):
    def test_create_short_url(self):
        short_url = ShortUrls.create_short_url("https://www.canada.ca", "test1234")
        assert short_url == "test1234"

    def test_create_short_url_with_existing_url__returns_same_shorten_url(self):
        url_a = ShortUrls.create_short_url("https://www.canada.ca", "test1234")
        url_b = ShortUrls.create_short_url("https://www.canada.ca", "test1234")
        assert url_a == url_b

    def test_get_short_url(self):
        ShortUrls.create_short_url("https://www.canada.ca", "test1234")
        short_url = ShortUrls.get_short_url("test1234")
        assert short_url["original_url"]["S"] == "https://www.canada.ca"

    def test_create_short_url_with_different_url_but_same_hash__raises_value_error_for_collision(
        self,
    ):
        with self.assertRaises(ValueError):
            ShortUrls.create_short_url("https://www.canada.ca", "test1234")
            ShortUrls.create_short_url("https://nrc.gc.ca", "test1234")
