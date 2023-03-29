from fastapi import (
    APIRouter,
    Body,
    HTTPException,
    status,
    Request,
    Form,
)
from fastapi.responses import HTMLResponse, RedirectResponse
import os
from pydantic import HttpUrl
from utils.helpers import resolve_short_url, validate_and_shorten_url
from utils.magic_link import create_magic_link, validate_magic_link
from utils.session import delete_cookie, set_cookie, validate_cookie
from fastapi.templating import Jinja2Templates


router = APIRouter()

templates = Jinja2Templates(directory="templates")


@router.get("/", response_class=HTMLResponse)
def home(request: Request):
    if validate_cookie(request):
        data = {"page": "Home Page", "button": "Shorten", "url": "", "logged_in": True}
        return templates.TemplateResponse(
            "index.html", {"request": request, "data": data}
        )
    else:
        return RedirectResponse(url="/login")


@router.post("/", response_class=HTMLResponse)
def create_shortened_url(
    request: Request,
    original_url: str = Form(),
):
    if validate_cookie(request):
        data = validate_and_shorten_url(original_url)
        return templates.TemplateResponse(
            "index.html", context={"request": request, "data": data}
        )
    else:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)


@router.get("/login", response_class=HTMLResponse)
def login(request: Request):
    data = {"page": "Login Page", "button": "Login", "url": ""}
    return templates.TemplateResponse("login.html", {"request": request, "data": data})


@router.post("/login", response_class=HTMLResponse)
def login_post(request: Request, email: str = Form(...)):
    domain = email.split("@").pop()
    result = {}
    if domain in os.getenv("ALLOWED_DOMAINS").split(","):
        result = create_magic_link(email)
    else:
        result["error"] = "Not a valid email address"
    data = {
        "page": "Login Page",
        "button": "Login",
        "error": result.get("error", None),
        "success": result.get("success", None),
    }
    return templates.TemplateResponse("login.html", {"request": request, "data": data})


@router.get("/logout", response_class=HTMLResponse)
def logout(request: Request):
    response = RedirectResponse(url="/login")
    delete_cookie(request, response)
    return response


@router.get("/magic_link", response_class=HTMLResponse)
def magic_link(request: Request, guid: str, email: str):
    result = validate_magic_link(guid, email)
    if "success" in result:
        response = RedirectResponse(url="/")
        set_cookie(response, email)
        return response
    else:
        data = {
            "page": "Magic Link Page",
            "button": "Magic Link",
            "url": "",
            "error": result.get("error", None),
        }
        return templates.TemplateResponse(
            "login.html", {"request": request, "data": data}
        )


@router.post("/v1", status_code=status.HTTP_201_CREATED)
def create_shortened_url_api(
    original_url: HttpUrl = Body(..., embed=True),
):
    resp = validate_and_shorten_url(original_url)
    if resp["status"] == "ERROR":
        raise HTTPException(status_code=400, detail=resp)
    return resp


@router.get("/{short_url}", response_class=HTMLResponse)
def redirect_to_site(short_url: str, request: Request):
    short_url_obj = resolve_short_url(short_url)
    if not short_url_obj:
        resp = templates.TemplateResponse("404.html", context={"request": request})
        resp.status_code = status.HTTP_404_NOT_FOUND
        return resp
    resp = templates.TemplateResponse(
        "redirect.html",
        context={
            "request": request,
            "data": {"url": short_url_obj["original_url"]["S"]},
        },
    )
    resp.status_code = status.HTTP_200_OK
    return resp
