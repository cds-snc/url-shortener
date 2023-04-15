from unittest.mock import patch, MagicMock
from utils import contact


@patch("utils.contact.notification_client")
@patch("utils.contact.NOTIFY_CONTACT_EMAIL", "notify_contact_email")
@patch("utils.contact.NOTIFY_CONTACT_TEMPLATE", "notify_contact_template")
def test_send_contact_email_returns_success(mock_notification_client):
    mock_client = MagicMock()
    mock_client.send_email_notification.return_value = True
    mock_notification_client.return_value = mock_client
    assert contact.send_contact_email("email", "subject", "details") == {
        "success": "success_contact_sent"
    }
    mock_client.send_email_notification.assert_called_once_with(
        email_address="notify_contact_email",
        template_id="notify_contact_template",
        personalisation={
            "contact_email": "email",
            "contact_subject": "subject",
            "contact_details": "details",
        },
    )


@patch("utils.contact.notification_client")
def test_send_contact_email_returns_error_on_failed_send(mock_notification_client):
    mock_client = MagicMock()
    mock_client.send_email_notification.side_effect = Exception("error")
    mock_notification_client.return_value = mock_client
    assert contact.send_contact_email("email", "subject", "details") == {
        "error": "error_contact_send_failed"
    }
