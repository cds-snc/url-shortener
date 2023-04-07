from utils import magic_link

from unittest.mock import patch

EMAIL = "foo@canada.ca"


@patch("utils.magic_link.check_if_exists")
def test_create_magic_link_returns_error_if_email_already_has_a_magic_link(
    mock_check_if_exists,
):
    mock_check_if_exists.return_value = True
    result = magic_link.create_magic_link(EMAIL)
    assert result == {"error": "error_email_has_magic_link"}


@patch("utils.magic_link.check_if_exists")
@patch("utils.magic_link.create")
def test_create_magic_link_returns_error_if_could_not_create_magic_link(
    mock_create, mock_check_if_exists
):
    mock_check_if_exists.return_value = False
    mock_create.return_value = [None, None]
    result = magic_link.create_magic_link(EMAIL)
    assert result == {"error": "error_create_magic_link"}


@patch("utils.magic_link.check_if_exists")
@patch("utils.magic_link.create")
@patch("utils.magic_link.notification_client")
def test_create_magic_link_returns_success_if_magic_link_created(
    mock_notification_client, mock_create, mock_check_if_exists
):
    mock_check_if_exists.return_value = False
    mock_create.return_value = ["guid", EMAIL]
    result = magic_link.create_magic_link(EMAIL)
    assert result == {"success": "success_magic_link_sent_email"}
    mock_notification_client.return_value.send_email_notification.assert_called_once()


@patch("utils.magic_link.check_if_exists")
@patch("utils.magic_link.create")
@patch("utils.magic_link.notification_client")
def test_create_magic_link_returns_error_if_notify_throws_an_error(
    mock_notification_client, mock_create, mock_check_if_exists
):
    mock_check_if_exists.return_value = False
    mock_create.return_value = ["guid", EMAIL]
    mock_notification_client.return_value.send_email_notification.side_effect = (
        Exception("Error")
    )
    result = magic_link.create_magic_link(EMAIL)
    assert result == {"error": "error_send_magic_link_email"}


@patch("utils.magic_link.get")
def test_validate_magic_link_returns_error_if_magic_link_is_not_valid(mock_get):
    mock_get.return_value = None
    result = magic_link.validate_magic_link("guid", EMAIL)
    assert result == {"error": "error_email_not_valid"}


@patch("utils.magic_link.get")
def test_validate_magic_link_returns_success_if_magic_link_is_valid(mock_get):
    mock_get.return_value = EMAIL
    result = magic_link.validate_magic_link("guid", EMAIL)
    assert result == {"success": "success_email_valid"}
    mock_get.assert_called_once_with("guid")


@patch("utils.magic_link.NotificationsAPIClient")
def test_notification_client(mock_notifications_api_client):
    assert (
        magic_link.notification_client() == mock_notifications_api_client.return_value
    )
