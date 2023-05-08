import time
import datetime
from unittest import TestCase
from models import ShortUrls


class TestCreateShortUrl(TestCase):
    def test_create_short_url(self):
        short_url = ShortUrls.create_short_url(
            "https://www.canada.ca", "test1234", "actor"
        )
        assert short_url == "test1234"

    def test_create_short_url_with_existing_url__returns_same_shorten_url(self):
        url_a = ShortUrls.create_short_url("https://www.canada.ca", "test1234", "actor")
        url_b = ShortUrls.create_short_url("https://www.canada.ca", "test1234", "actor")
        assert url_a == url_b

    def test_get_short_url(self):
        ShortUrls.create_short_url("https://www.canada.ca", "test", "actor")
        short_url = ShortUrls.get_short_url("test")
        assert short_url["original_url"]["S"] == "https://www.canada.ca"
        assert short_url["created_by"]["S"] == "actor"
        assert short_url["click_count"]["N"] == "0"
        short_url = ShortUrls.get_short_url("test")
        assert short_url["click_count"]["N"] == "1"
        short_url = ShortUrls.get_short_url("test")
        assert short_url["click_count"]["N"] == "2"

    def test_update_last_access_at(self):
        """Test that we are setting the last_access_date properly and it is being updated each time the shortned url is retrieved"""
        ShortUrls.create_short_url("https://www.canada.ca", "xyz", "actor")
        time.sleep(1)
        short_url = ShortUrls.get_short_url("xyz")
        assert short_url["last_access_date"]["N"] == short_url["created_at"]["N"]
        short_url = ShortUrls.get_short_url("xyz")
        time.sleep(1)
        assert short_url["last_access_date"]["N"] != short_url["created_at"]["N"]
        previous_last_access_date = int(short_url["last_access_date"]["N"])
        short_url = ShortUrls.get_short_url("xyz")
        assert short_url["last_access_date"]["N"] != previous_last_access_date

    def test_update_ttl_time(self):
        """Test that we are setting the ttl properly and it is being updated each time the shortned url is retrieved"""
        ShortUrls.create_short_url("https://www.canada.ca", "abc", "actor")
        time.sleep(1)
        short_url = ShortUrls.get_short_url("abc")
        previous_ttl = int(short_url["ttl"]["N"])
        short_url = ShortUrls.get_short_url("abc")
        assert short_url["ttl"]["N"] != str(previous_ttl)

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
            ShortUrls.create_short_url("https://www.canada.ca", "test1234", "actor")
            ShortUrls.create_short_url("https://nrc.gc.ca", "test1234", "actor")
