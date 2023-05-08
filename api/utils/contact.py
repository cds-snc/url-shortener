import os
import traceback
from logger import log
from utils.helpers import notification_client

NOTIFY_CONTACT_EMAIL = os.environ.get("NOTIFY_CONTACT_EMAIL", None)
NOTIFY_CONTACT_TEMPLATE = os.environ.get("NOTIFY_CONTACT_TEMPLATE", None)


def send_contact_email(
    contact_email: str,
    contact_subject: str,
    contact_details: str,
):
    """
    Sends an email to the contact email address.
    """
    try:
        client = notification_client()
        client.send_email_notification(
            email_address=NOTIFY_CONTACT_EMAIL,
            template_id=NOTIFY_CONTACT_TEMPLATE,
            personalisation={
                "contact_email": contact_email,
                "contact_subject": contact_subject,
                "contact_details": contact_details[:10000],
            },
        )
    except Exception:
        log.error("Failed to send contact email: %s", traceback.format_exc())
        return {"error": "error_contact_send_failed"}
    return {"success": "success_contact_sent"}
