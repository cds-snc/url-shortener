import os

from models.MagicLinks import create, delete, get, check_if_exists
from notifications_python_client.notifications import NotificationsAPIClient
from logger import log


NOTIFY_API_KEY = os.environ.get("NOTIFY_API_KEY", None)
NOTIFY_MAGIC_LINK_TEMPLATE = os.environ.get("NOTIFY_MAGIC_LINK_TEMPLATE", None)
SHORTENER_DOMAIN = os.environ.get("SHORTENER_DOMAIN", None)


def create_magic_link(email):
    if not check_if_exists(email):
        [guid, email] = create(email)
        if guid:
            try:
                client = notification_client()
                magic_link = f"{SHORTENER_DOMAIN}magic_link?guid={guid}&email={email}"
                client.send_email_notification(
                    email_address=email,
                    template_id=NOTIFY_MAGIC_LINK_TEMPLATE,
                    personalisation={"magic_link": magic_link},
                )
            except Exception as e:
                log.error(e)
                return {"error": "Could not send magic link to email."}
            return {"success": "Magic link sent to email."}
        else:
            return {"error": "Could not create magic link."}
    else:
        return {
            "error": "Email already has a magic link. Please wait 5 minutes before requesting a new one."
        }


def validate_magic_link(guid, email):
    link_email = get(guid)
    if email == link_email:
        delete(guid)
        return {"success": "Magic link is valid."}
    else:
        return {"error": "Magic link is not valid."}


def notification_client():
    return NotificationsAPIClient(
        NOTIFY_API_KEY, base_url="https://api.notification.canada.ca"
    )
