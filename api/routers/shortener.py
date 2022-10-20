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
from models.AllowedDomains import AllowedDomains
from utils.helpers import generate_short_url, return_short_url, is_domain_allowed, is_valid_url
from fastapi.templating import Jinja2Templates
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

router = APIRouter()

templates = Jinja2Templates(directory="templates")

@router.post("/", response_class=HTMLResponse)
def create_shortened_url(
	request: Request,
	db_session: Session = Depends(get_db_session),
	original_url: str = Form(...)):
	accept = request.headers["accept"]
	print(accept)
	try:
		# Check to see if the url confronts to a valid format. If not then display error.
		if (not is_valid_url(original_url)):
			data = {
				"error": "Unable to shorten link. Invalid URL.",
				"url": original_url
			}
		# Else if the domain is not allowed, display error and link to GC Forms page
		elif (not is_domain_allowed(original_url, db_session)):
			forms_url = os.getenv("FORMS_URL")
			data = {
				"error": "URL is not registered in our system as an Official GC Domain.",
				"form_url": forms_url,
				"url": original_url
			}
		# Else, we are all good to shorten!
		else:
			short_url = return_short_url(original_url, db_session)
			SHORTENER_DOMAIN = os.getenv("SHORTENER_DOMAIN") or None
			data = {
				"short_url": short_url,
				"url": SHORTENER_DOMAIN + short_url,
			}
	except Exception as err:
		data = {
			"error": f"Error in processing shortened url {err}"
			}
	if len(accept.split(",")) > 1:
		return templates.TemplateResponse("index.html", context={"request":request, "data":data})
	else:
		return {"status": "NOT OK", "short_url": short_url}


@router.post('/shorten', status_code = status.HTTP_201_CREATED)
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
		return RedirectResponse(url = short_url_obj.original_url, status_code = status.HTTP_301_MOVED_PERMANENTLY)
	except SQLAlchemyError as err:
		log.error(err)
		return {"error": "error retrieving link details"}
	

