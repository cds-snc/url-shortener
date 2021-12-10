from database.db import get_db_session
from fastapi import APIRouter, Depends, Body, HTTPException, Response, status
from datetime import datetime, timezone
from sqlalchemy.orm import Session
#from logger import log
import logging
from pydantic import HttpUrl
from models.ShortUrl import ShortUrls
from utils.helpers import generate_short_url

router = APIRouter()

@router.post('/shorten')
def create_shortened_url(
	db_session: Session = Depends(get_db_session),
	original_url: HttpUrl = Body(..., embed=True)
):
	
	try:
		short_url = generate_short_url(original_url)
		short_url_obj = ShortUrl(
			original_url = original_url, short_url = short_url)

		db_session.add(short_url_obj)
		db_session.commit()

	except Exception as err:
		log.error(err)
		response.status_code = status.HTTP_502_BAD_GATEWAY
		return{"error": f"error in processing shortened url"}

	return {"status": "OK", "short_url": short_url}



@router.get('/{short_url}')
def redirect_to_site (
	short_url: str,
	db_session: Session = Depends(get_db_session)
):


	try:
		short_url_obj = db_session.query(ShortUrl).filter(ShortUrl.short_link == short_link).one_or_none()
		if short_url_obj is None:
			raise HTTPException(
				status_code=404,
				detail = 'The given link does not exist.'
			)
		return RedirectResponse(url=short_url_obj.original_url)
	except SQLAlchemyError as err:
		log.error(err)
		response.status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
		return {"error": "error retrieving link details"}
	

