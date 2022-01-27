from database.db import get_db_session
from datetime import datetime, timezone
from fastapi import APIRouter, Depends, Body, HTTPException, Response, status, Request, Form
from fastapi.responses import RedirectResponse, HTMLResponse
from datetime import datetime, timezone
from sqlalchemy.orm import Session
from logger import log
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import Session
from pydantic import HttpUrl
from models.ShortUrls import ShortUrls
from utils.helpers import generate_short_url
from fastapi.templating import Jinja2Templates



router = APIRouter()

templates = Jinja2Templates(directory="templates")

@router.post("/gui_shorten", response_class=HTMLResponse)
def create_shortened_url(
	request: Request,
	db_session: Session = Depends(get_db_session),
	original_url: str = Form(...)):
	try:
		timestamp = datetime.now().replace(tzinfo=timezone.utc).timestamp()
		short_url = generate_short_url(original_url, timestamp)
		print(f"This is the short url {short_url}")
		short_url_obj = ShortUrls(
			original_url = original_url, short_url = short_url)
		db_session.add(short_url_obj)
		db_session.commit()
		data = {
			"short_url": short_url,
			"url": "http://localhost:8000/" + short_url,
			"label": "Enter the url to shorten",
			"button": "Shorten now"
		}

	except Exception as err:
		data = {
			"error" : "Error in processing shortened url"
			}
	return templates.TemplateResponse("index.html", context={"request":request, "data":data})



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
		#response.status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
		return {"error": "error retrieving link details"}
	

