import os
import traceback
from email.utils import parseaddr
from models.MagicLinks import create, get, check_if_exists
from logger import log

from utils.helpers import notification_client

EMAIL_DOMAIN_MAX_LENGTH = 255
EMAIL_LOCAL_MAX_LENGTH = 64
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
            except Exception:
                log.error("Failed to send magic link: %s", traceback.format_exc())
                result = {"error": "error_send_magic_link_email"}
        else:
            result = {"error": "error_create_magic_link"}
    else:
        result = {"error": "error_email_has_magic_link"}
    log.info("Magic link create for email '%s': %s", email, result)
    return result


def get_email_domain(email):
    """
    Performs simple email validation on a provided email address
    and returns the domain if it looks valid.
    """
    email_domain = None
    email_parsed = parseaddr(email)
    if "@" in email_parsed[1]:
        email_parts = email_parsed[1].split("@")
        if (
            len(email_parts) == 2
            and len(email_parts[0]) > 0
            and len(email_parts[0]) < EMAIL_LOCAL_MAX_LENGTH
            and len(email_parts[1]) > 0
            and len(email_parts[1]) < EMAIL_DOMAIN_MAX_LENGTH
        ):
            email_domain = email_parts[1]
    return email_domain


def is_allowed_email_domain(domain_list, domain):
    """
    Returns True if the given domain is a subdomain of any of the domains in the list.
    """
    if domain is None:
        return False
    for d in domain_list:
        if domain.endswith("." + d) or domain == d:
            return True
    return False


def validate_magic_link(guid, email):
    link_email = get(guid)
    if email == link_email:
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
