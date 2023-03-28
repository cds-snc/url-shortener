from models import Session

from unittest.mock import patch


@patch("models.Session.client.put_item")
def test_create_returns_session_id(mock_put_item):
    mock_put_item.return_value = {"ResponseMetadata": {"HTTPStatusCode": 200}}
    assert Session.create("foo", "bar") == "foo"


@patch("models.Session.client.put_item")
def test_create_returns_false_if_put_item_fails(mock_put_item):
    mock_put_item.return_value = {"ResponseMetadata": {"HTTPStatusCode": 400}}
    assert Session.create("foo", "bar") is False


@patch("models.Session.client.get_item")
def test_read_returns_item_if_get_item_succeeds(mock_get_item):
    mock_get_item.return_value = {
        "ResponseMetadata": {"HTTPStatusCode": 200},
        "Item": {"foo": "bar"},
    }
    assert Session.read("foo") == {"foo": "bar"}


@patch("models.Session.client.get_item")
def test_read_returns_none_if_get_item_fails(mock_get_item):
    mock_get_item.return_value = {
        "ResponseMetadata": {"HTTPStatusCode": 400},
    }
    assert Session.read("foo") is None


@patch("models.Session.client.update_item")
def test_update_returns_true_if_update_item_succeeds(mock_update_item):
    mock_update_item.return_value = {"ResponseMetadata": {"HTTPStatusCode": 200}}
    assert Session.update("foo", "bar") == "foo"


@patch("models.Session.client.update_item")
def test_update_returns_false_if_update_item_fails(mock_update_item):
    mock_update_item.return_value = {"ResponseMetadata": {"HTTPStatusCode": 400}}
    assert Session.update("foo", "bar") is None


@patch("models.Session.client.delete_item")
def test_delete_returns_true_if_delete_item_succeeds(mock_delete_item):
    mock_delete_item.return_value = {"ResponseMetadata": {"HTTPStatusCode": 200}}
    assert Session.delete("foo") == "foo"


@patch("models.Session.client.delete_item")
def test_delete_returns_false_if_delete_item_fails(mock_delete_item):
    mock_delete_item.return_value = {"ResponseMetadata": {"HTTPStatusCode": 400}}
    assert Session.delete("foo") is None
