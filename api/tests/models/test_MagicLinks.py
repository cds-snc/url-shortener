from models import MagicLinks

from unittest.mock import patch


@patch("models.MagicLinks.client.put_item")
def test_create_returns_guid_and_email(mock_put_item):
    mock_put_item.return_value = {"ResponseMetadata": {"HTTPStatusCode": 200}}
    [guid, email] = MagicLinks.create("foo@canada.ca")
    assert len(guid) == 36
    assert email == "foo@canada.ca"


@patch("models.MagicLinks.client.put_item")
def test_create_returns_none_if_put_item_fails(mock_put_item):
    mock_put_item.return_value = {"ResponseMetadata": {"HTTPStatusCode": 400}}
    [guid, email] = MagicLinks.create("foo@canada.ca")
    assert guid is None
    assert email is None


@patch("models.MagicLinks.client.delete_item")
def test_delete_returns_true_if_delete_item_succeeds(mock_delete_item):
    mock_delete_item.return_value = {"ResponseMetadata": {"HTTPStatusCode": 200}}
    assert MagicLinks.delete("foo") is True


@patch("models.MagicLinks.client.delete_item")
def test_delete_returns_false_if_delete_item_fails(mock_delete_item):
    mock_delete_item.return_value = {"ResponseMetadata": {"HTTPStatusCode": 400}}
    assert MagicLinks.delete("foo") is False


@patch("models.MagicLinks.client.get_item")
def test_get_returns_email_if_get_item_succeeds(mock_get_item):
    mock_get_item.return_value = {
        "ResponseMetadata": {"HTTPStatusCode": 200},
        "Item": {"email": {"S": "MODEL_PREFIX/foo@canada.ca"}},
    }
    assert MagicLinks.get("guid") == "foo@canada.ca"


@patch("models.MagicLinks.client.get_item")
def test_get_returns_none_if_get_item_fails(mock_get_item):
    mock_get_item.return_value = {
        "ResponseMetadata": {"HTTPStatusCode": 400},
    }
    assert MagicLinks.get("guid") is None


@patch("models.MagicLinks.client.get_item")
@patch("models.MagicLinks.delete")
def test_get_returns_none_if_get_item_succeeds_but_ttl_has_passed(
    mock_delete, mock_get_item
):
    mock_get_item.return_value = {
        "ResponseMetadata": {"HTTPStatusCode": 200},
        "Item": {
            "email": {"S": "MODEL_PREFIX/foo@canada.ca"},
            "ttl": {"N": "0"},
        },
    }
    assert MagicLinks.get("guid") is None
    mock_delete.assert_called_once()


@patch("models.MagicLinks.client.query")
def test_check_if_exists_returns_true_if_query_succeeds(mock_query):
    mock_query.return_value = {
        "ResponseMetadata": {"HTTPStatusCode": 200},
        "Items": [{"email": {"S": "MODEL_PREFIX/foo@canada.ca"}}],
    }
    assert MagicLinks.check_if_exists("foo@canada.ca") is True


@patch("models.MagicLinks.client.query")
def test_check_if_exists_returns_false_if_query_fails(mock_query):
    mock_query.return_value = {
        "ResponseMetadata": {"HTTPStatusCode": 400},
    }
    assert MagicLinks.check_if_exists("foo@canada.ca") is False
