import os
import re

from typing import Annotated, Optional
from fastapi import (
    APIRouter,
    Body,
    Depends,
    Header,
    HTTPException,
    status,
    Request,
    Form,
)
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from pydantic import HttpUrl

from utils.auth_token import validate_auth_token
from utils.contact import send_contact_email
from utils.helpers import redact_value, resolve_short_url, validate_and_shorten_url
from utils.i18n import (
    LANGUAGES,
    Locale,
    get_language,
    get_locale_from_header,
    get_locale_from_path,
    get_locale_order,
)
from utils.magic_link import create_magic_link, validate_magic_link
from utils.session import (
    delete_cookie,
    set_cookie,
    validate_cookie,
    validate_user_email,
)


router = APIRouter()

templates = Jinja2Templates(directory="templates")

SHORTENER_PATH_LENGTH = int(os.environ.get("SHORTENER_PATH_LENGTH", "0"))
SHORTENER_PATH_REGEX = re.compile(f"^[a-zA-Z0-9]{{{SHORTENER_PATH_LENGTH}}}$")


@router.get("/", response_class=HTMLResponse, include_in_schema=False)
async def force_lang(accept_language: str | None = Header(None)):
    """
    Root URL.  Redirects to the user's preferred language based on the Accept-Language header.
    """
    user_locale = get_locale_from_header(accept_language)
    return RedirectResponse(f"/{user_locale}")


# We don't use a dynamic `locale` path parameter here because we need to differentiate
# the top level language routes from the shortened URL redirect route further down.
@router.get("/en", response_class=HTMLResponse)
@router.get("/fr", response_class=HTMLResponse)
def home(request: Request):
    """
    Root URL for each language.  Renders the home page for logged in and logged out users.
    """
    locale = get_locale_from_path(request.url.path)
    language = get_language(locale)
    if validate_cookie(request):
        data = {"logged_in": True}
        return templates.TemplateResponse(
            "index.html", {"request": request, "data": data, "i18n": language}
        )
    else:
        return RedirectResponse(url=f"/{locale}/{language['login_path']}")


@router.post("/en", response_class=HTMLResponse)
@router.post("/fr", response_class=HTMLResponse)
def create_shortened_url(
    request: Request,
    original_url: Optional[str] = Form(""),
    user_email: str = Depends(validate_user_email),
):
    """
    Generates a shortened URL for the given original URL.  This route is used by the frontend.
    """
    locale = get_locale_from_path(request.url.path)
    data = validate_and_shorten_url(original_url, user_email)
    data["logged_in"] = True
    return templates.TemplateResponse(
        "index.html",
        context={"request": request, "data": data, "i18n": get_language(locale)},
    )


@router.get("/{locale}/connexion", response_class=HTMLResponse)
@router.get("/{locale}/login", response_class=HTMLResponse)
def login(locale: Locale, request: Request):
    """
    Renders the login page.
    """
    return templates.TemplateResponse(
        "login.html", {"request": request, "data": {}, "i18n": get_language(locale)}
    )


@router.post("/{locale}/connexion", response_class=HTMLResponse)
@router.post("/{locale}/login", response_class=HTMLResponse)
def login_post(locale: Locale, request: Request, email: Optional[str] = Form("")):
    """
    Attempts to generate and send a magic login link to the given email address.
    """
    domain = email.split("@").pop()
    result = {}
    if domain in os.getenv("ALLOWED_DOMAINS").split(","):
        result = create_magic_link(email)
    else:
        result["error"] = "error_invalid_email_address"
    data = {
        "error": result.get("error", None),
        "success": result.get("success", None),
    }
    return templates.TemplateResponse(
        "login.html", {"request": request, "data": data, "i18n": get_language(locale)}
    )


@router.get("/{locale}/deconnexion", response_class=HTMLResponse)
@router.get("/{locale}/logout", response_class=HTMLResponse)
def logout(locale: Locale, request: Request):
    """
    Logs the user out by deleting the session cookie.
    """
    language = get_language(locale)
    response = RedirectResponse(url=f"/{locale}/{language['login_path']}")
    delete_cookie(request, response)
    return response


@router.get("/{locale}/lien-magique", response_class=HTMLResponse)
@router.get("/{locale}/magic-link", response_class=HTMLResponse)
def magic_link(locale: Locale, request: Request, guid: str, email: str):
    """
    Validates the magic link and logs the user in on success.
    """
    result = validate_magic_link(guid, email)
    if "success" in result:
        response = RedirectResponse(url=f"/{locale}")
        set_cookie(response, email)
        return response
    else:
        data = {
            "error": result.get("error", None),
        }
        return templates.TemplateResponse(
            "login.html",
            {"request": request, "data": data, "i18n": get_language(locale)},
        )


@router.get("/lang/{new_locale}", response_class=HTMLResponse)
def change_language(new_locale: Locale):
    """
    Changes the language of the site.
    """
    return RedirectResponse(url=f"/{new_locale}")


@router.post("/v1", status_code=status.HTTP_201_CREATED)
def create_shortened_url_api(
    auth_token: Annotated[str, Depends(validate_auth_token)],
    original_url: HttpUrl = Body(..., embed=True),
):
    """
    API endpoint for generating a shortened URL.  It requires a valid auth token.
    """
    resp = validate_and_shorten_url(original_url, redact_value(auth_token))
    if resp["status"] == "ERROR":
        raise HTTPException(status_code=400, detail=resp)
    return resp


@router.get(
    "/{locale}/contact", response_class=HTMLResponse, status_code=status.HTTP_200_OK
)
def contact(
    locale: Locale,
    request: Request,
    subject: Optional[str] = None,
    user_email: str = Depends(validate_user_email),
):
    """
    Renders the contact page for logged in users.
    """
    return templates.TemplateResponse(
        "contact.html",
        context={
            "request": request,
            "data": {
                "logged_in": True,
                "user_email": user_email,
                "contact_subject": "Register a new domain"
                if subject == "domain"
                else "",
            },
            "i18n": get_language(locale),
        },
    )


@router.post(
    "/{locale}/contact", response_class=HTMLResponse, status_code=status.HTTP_200_OK
)
def contact_send(
    locale: Locale,
    request: Request,
    contact_subject: Annotated[str, Form()],
    contact_details: Annotated[str, Form()],
    user_email: str = Depends(validate_user_email),
):
    """
    Contact form submissions.
    """
    result = send_contact_email(user_email, contact_subject, contact_details)
    return templates.TemplateResponse(
        "contact.html",
        context={
            "request": request,
            "data": {
                "logged_in": True,
                "user_email": user_email,
                "contact_subject": contact_subject,
                "contact_details": contact_details,
            }
            | result,
            "i18n": get_language(locale),
        },
    )


@router.get("/{short_url}", response_class=HTMLResponse, status_code=status.HTTP_200_OK)
def redirect_to_site(
    short_url: str, request: Request, accept_language: str | None = Header(None)
):
    """
    Handles shortened URLs and presents the user with a redirect notice page.
    If the short URL path segment is not valid or can't be found, the user
    gets a 404 page.  This is required as this route is a catch-all and
    will match all root level requests.
    """
    user_locale = get_locale_from_header(accept_language)
    locale_order = get_locale_order(user_locale)
    language = get_language(user_locale)
    short_url_obj = None
    if SHORTENER_PATH_REGEX.match(short_url):
        short_url_obj = resolve_short_url(short_url)

    if not short_url_obj:
        resp = templates.TemplateResponse(
            "404.html",
            context={
                "request": request,
                "i18n": language,
                "i18n_all": LANGUAGES,
                "locale_order": locale_order,
            },
        )
        resp.status_code = status.HTTP_404_NOT_FOUND
        return resp

    resp = templates.TemplateResponse(
        "redirect.html",
        context={
            "request": request,
            "data": {"url": short_url_obj["original_url"]["S"]},
            "i18n": language,
            "i18n_all": LANGUAGES,
            "locale_order": locale_order,
        },
    )
    resp.status_code = status.HTTP_200_OK
    return resp
