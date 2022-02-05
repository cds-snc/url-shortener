from database.db import get_db_session
from datetime import datetime, timezone
from fastapi import APIRouter, Depends, Body, HTTPException, Response, status, Request, Form
from fastapi.responses import RedirectResponse, HTMLResponse
from sqlalchemy.orm import Session
from logger import log
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import Session
from pydantic import HttpUrl
from models.ShortUrls import ShortUrls
from utils.helpers import generate_short_url, return_short_url
from fastapi.templating import Jinja2Templates

router = APIRouter()

templates = Jinja2Templates(directory="templates")

@router.post("/", response_class=HTMLResponse)
def create_shortened_url(
	request: Request,
	db_session: Session = Depends(get_db_session),
	original_url: str = Form(...)):
	try:
		short_url = return_short_url(original_url, db_session)
		data = {
			"short_url": short_url,
			"url": "http://localhost:8000/" + short_url,
			"button": "Shorten now"
		}
	except Exception as err:
		data = {
			"error" : "Error in processing shortened url"
			}
	return templates.TemplateResponse("index.html", context={"request":request, "data":data})


@router.post('/shorten')
def create_shortened_url(
	db_session: Session = Depends(get_db_session),
	original_url: HttpUrl = Body(..., embed=True)):
	try:
		short_url = return_short_url(original_url, db_session)
		return {"status": "OK", "short_url": short_url}
	except Exception as err:
		return{"error": f"error in processing shortened url"}

@router.get('/{short_url}')
def redirect_to_site (
	short_url: str,
	db_session: Session = Depends(get_db_session)
):
	try:
		short_url_obj = db_session.query(ShortUrls).filter(ShortUrls.short_url == short_url).first()
		if short_url_obj is None:
			raise HTTPException(
				status_code=404,
				detail = 'The given link does not exist.'
			)
		return RedirectResponse(url=short_url_obj.original_url)
	except SQLAlchemyError as err:
		log.error(err)
		return {"error": "error retrieving link details"}
	

