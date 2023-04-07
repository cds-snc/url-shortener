from typing import Annotated, Optional
from fastapi import (
    APIRouter,
    Body,
    Depends,
    HTTPException,
    status,
    Request,
    Form,
)
from fastapi.responses import HTMLResponse, RedirectResponse
import os
from pydantic import HttpUrl
from utils.auth_token import validate_auth_token
from utils.helpers import resolve_short_url, validate_and_shorten_url
from utils.i18n import (
    DEFAULT_LOCALE,
    LANGUAGES,
    Locale,
    get_language,
    get_locale_from_path,
)
from utils.magic_link import create_magic_link, validate_magic_link
from utils.session import delete_cookie, set_cookie, validate_cookie
from fastapi.templating import Jinja2Templates


router = APIRouter()

templates = Jinja2Templates(directory="templates")


@router.get("/", response_class=HTMLResponse, include_in_schema=False)
async def force_lang():
    return RedirectResponse(f"/{DEFAULT_LOCALE}")


# We don't use a dynamic `locale` path parameter here because we need to differentiate
# the top level language routes from the shortened URL redirect route further down.
@router.get("/en", response_class=HTMLResponse)
@router.get("/fr", response_class=HTMLResponse)
def home(request: Request):
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
):
    locale = get_locale_from_path(request.url.path)
    if validate_cookie(request):
        data = validate_and_shorten_url(original_url)
        data["logged_in"] = True
        return templates.TemplateResponse(
            "index.html",
            context={"request": request, "data": data, "i18n": get_language(locale)},
        )
    else:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)


@router.get("/{locale}/connexion", response_class=HTMLResponse)
@router.get("/{locale}/login", response_class=HTMLResponse)
def login(locale: Locale, request: Request):
    return templates.TemplateResponse(
        "login.html", {"request": request, "data": {}, "i18n": get_language(locale)}
    )


@router.post("/{locale}/connexion", response_class=HTMLResponse)
@router.post("/{locale}/login", response_class=HTMLResponse)
def login_post(locale: Locale, request: Request, email: Optional[str] = Form("")):
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
    language = get_language(locale)
    response = RedirectResponse(url=f"/{locale}/{language['login_path']}")
    delete_cookie(request, response)
    return response


@router.get("/{locale}/lien-magique", response_class=HTMLResponse)
@router.get("/{locale}/magic-link", response_class=HTMLResponse)
def magic_link(locale: Locale, request: Request, guid: str, email: str):
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
    return RedirectResponse(url=f"/{new_locale}")


@router.post("/v1", status_code=status.HTTP_201_CREATED)
def create_shortened_url_api(
    authenticated: Annotated[bool, Depends(validate_auth_token)],
    original_url: HttpUrl = Body(..., embed=True),
):
    resp = validate_and_shorten_url(original_url)
    if resp["status"] == "ERROR":
        raise HTTPException(status_code=400, detail=resp)
    return resp


@router.get("/{short_url}", response_class=HTMLResponse)
def redirect_to_site(short_url: str, request: Request):
    language_en = get_language(Locale.en)
    short_url_obj = resolve_short_url(short_url)
    if not short_url_obj:
        resp = templates.TemplateResponse(
            "404.html",
            context={
                "request": request,
                "i18n": language_en,
                "i18n_all": LANGUAGES,
            },
        )
        resp.status_code = status.HTTP_404_NOT_FOUND
        return resp
    resp = templates.TemplateResponse(
        "redirect.html",
        context={
            "request": request,
            "data": {"url": short_url_obj["original_url"]["S"]},
            "i18n": language_en,
            "i18n_all": LANGUAGES,
        },
    )
    resp.status_code = status.HTTP_200_OK
    return resp
