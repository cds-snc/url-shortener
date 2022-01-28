from fastapi import FastAPI, Request, Form
from os import environ
from pydantic import BaseSettings
from routers import shortener, shortener_gui
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse



class Settings(BaseSettings):
	openapi_url: str = environ.get("OPENAPI_URL", "")

description = """ 
API to shorten a url
"""

# initialize the app with title, version and url
app = FastAPI(
	title="API shortener",
	description= description,
	version="0.0.1",
)

# include other routes
app.include_router(shortener.router)
app.include_router(shortener_gui.router)

templates = Jinja2Templates(directory="templates")


@app.get("/", response_class=HTMLResponse)
async def home(request: Request):
	data = {
		"page": "Home Page",
		"button": "Shorten Now",
		"label": "Enter the url to shorten",
		"url": ""
		}
	return templates.TemplateResponse("index.html", {"request":request, "data": data})
