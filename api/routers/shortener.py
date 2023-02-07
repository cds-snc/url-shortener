from database.db import get_db_session
from fastapi import (
    APIRouter,
    Depends,
    Body,
    HTTPException,
    status,
    Request,
    Form,
)
from fastapi.responses import RedirectResponse, HTMLResponse
from sqlalchemy.orm import Session

from pydantic import HttpUrl
from utils.helpers import resolve_short_url, validate_and_shorten_url
from fastapi.templating import Jinja2Templates
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

router = APIRouter()

templates = Jinja2Templates(directory="templates")


@router.get("/", response_class=HTMLResponse)
async def home(request: Request):
    data = {"page": "Home Page", "button": "Shorten", "url": ""}
    return templates.TemplateResponse("index.html", {"request": request, "data": data})


@router.post("/", response_class=HTMLResponse)
def create_shortened_url(
    request: Request,
    db_session: Session = Depends(get_db_session),
    original_url: str = Form(),
):
    data = validate_and_shorten_url(original_url, db_session)
    return templates.TemplateResponse(
        "index.html", context={"request": request, "data": data}
    )


@router.post("/shorten", status_code=status.HTTP_201_CREATED)
def create_shortened_url_api(
    db_session: Session = Depends(get_db_session),
    original_url: HttpUrl = Body(..., embed=True),
):
    resp = validate_and_shorten_url(original_url, db_session)
    if resp["status"] == "ERROR":
        raise HTTPException(status_code=400, detail=resp)
    return resp


@router.get("/{short_url}")
def redirect_to_site(short_url: str, db_session: Session = Depends(get_db_session)):
    short_url_obj = resolve_short_url(short_url, db_session)
    if not short_url_obj:
        raise HTTPException(status_code=404, detail="The given link does not exist.")
    return RedirectResponse(
        url=short_url_obj.original_url,
        status_code=status.HTTP_302_FOUND,
    )
