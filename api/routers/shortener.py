from fastapi import (
    APIRouter,
    Body,
    HTTPException,
    status,
    Request,
    Form,
)
from fastapi.responses import HTMLResponse

from pydantic import HttpUrl
from utils.helpers import resolve_short_url, validate_and_shorten_url
from fastapi.templating import Jinja2Templates


router = APIRouter()

templates = Jinja2Templates(directory="templates")


@router.get("/", response_class=HTMLResponse)
async def home(request: Request):
    data = {"page": "Home Page", "button": "Shorten", "url": ""}
    return templates.TemplateResponse("index.html", {"request": request, "data": data})


@router.post("/", response_class=HTMLResponse)
def create_shortened_url(
    request: Request,
    original_url: str = Form(),
):
    data = validate_and_shorten_url(original_url)
    return templates.TemplateResponse(
        "index.html", context={"request": request, "data": data}
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
