import os

from models.MagicLinks import create, delete, get, check_if_exists
from logger import log

from utils.helpers import notification_client

NOTIFY_MAGIC_LINK_TEMPLATE = os.environ.get("NOTIFY_MAGIC_LINK_TEMPLATE", None)
SHORTENER_DOMAIN = os.environ.get("SHORTENER_DOMAIN", None)


def create_magic_link(email):
    if not check_if_exists(email):
        [guid, email] = create(email)
        if guid:
            try:
                client = notification_client()
                client.send_email_notification(
                    email_address=email,
                    template_id=NOTIFY_MAGIC_LINK_TEMPLATE,
                    personalisation={
                        "magic_link_en": f"{SHORTENER_DOMAIN}en/magic-link?guid={guid}&email={email}",
                        "magic_link_fr": f"{SHORTENER_DOMAIN}fr/lien-magique?guid={guid}&email={email}",
                    },
                )
            except Exception as error:
                log.error(error)
                return {"error": "error_send_magic_link_email"}
            return {"success": "success_magic_link_sent_email"}
        else:
            return {"error": "error_create_magic_link"}
    else:
        return {"error": "error_email_has_magic_link"}


def validate_magic_link(guid, email):
    link_email = get(guid)
    if email == link_email:
        delete(guid)
        return {"success": "success_email_valid"}
    else:
        log.warning("SUSPICIOUS: attempted login with invalid magic link")
        return {"error": "error_email_not_valid"}
