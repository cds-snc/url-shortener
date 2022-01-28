from database.db import get_db_session
from datetime import datetime, timezone
from fastapi import APIRouter, Depends, Body, HTTPException, Response, status
from fastapi.responses import RedirectResponse
from datetime import datetime, timezone
from sqlalchemy.orm import Session
from logger import log
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import Session
from pydantic import HttpUrl
from models.ShortUrls import ShortUrls
from utils.helpers import generate_short_url

router = APIRouter()

@router.post('/shorten')
def create_shortened_url(
	db_session: Session = Depends(get_db_session),
	original_url: HttpUrl = Body(..., embed=True)):
	
	try:
		print("in shortened url")
		timestamp = datetime.now().replace(tzinfo=timezone.utc).timestamp()
		short_url = generate_short_url(original_url, timestamp)
		print(f"This is the short url {short_url}")
		short_url_obj = ShortUrls(
			original_url = original_url, short_url = short_url)

		db_session.add(short_url_obj)
		db_session.commit()

	except Exception as err:
		return{"error": f"error in processing shortened url"}

	return {"status": "OK", "short_url": short_url}



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
	

