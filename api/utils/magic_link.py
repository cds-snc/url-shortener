import os

from models.MagicLinks import create, delete, get, check_if_exists
from logger import log

from utils.helpers import notification_client

NOTIFY_MAGIC_LINK_TEMPLATE = os.environ.get("NOTIFY_MAGIC_LINK_TEMPLATE", None)
SHORTENER_DOMAIN = os.environ.get("SHORTENER_DOMAIN", None)


def create_magic_link(email):
    result = {}
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
                result = {"success": "success_magic_link_sent_email"}
            except Exception as error:
                log.error(error)
                result = {"error": "error_send_magic_link_email"}
        else:
            result = {"error": "error_create_magic_link"}
    else:
        result = {"error": "error_email_has_magic_link"}
    log.info("Magic link create for email '%s': %s", email, result)
    return result


def validate_magic_link(guid, email):
    link_email = get(guid)
    if email == link_email:
        delete(guid)
        result = {"success": "success_email_valid"}
    else:
        log.warning("SUSPICIOUS: attempted login with invalid magic link")
        result = {"error": "error_email_not_valid"}
    log.info(
        "Magic link validate for guid '%s' and email '%s': %s",
        guid,
        email,
        result,
    )
    return result
