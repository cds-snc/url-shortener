from fastapi import FastAPI, Request, Form
from os import environ
from pydantic import BaseSettings
from routers import shortener
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles


class Settings(BaseSettings):
    openapi_url: str = environ.get("OPENAPI_URL", "")


description = """ 
API to shorten a url
"""

# initialize the app with title, version and url
app = FastAPI(
    title="API shortener",
    description=description,
    version="0.0.1",
)

# include other routes
app.include_router(shortener.router)

templates = Jinja2Templates(directory="templates")

# Mount static directory
app.mount("/static", StaticFiles(directory="static"), name="static")


@app.get("/", response_class=HTMLResponse)
async def home(request: Request):
    data = {"page": "Home Page", "button": "Shorten", "url": ""}
    return templates.TemplateResponse("index.html", {"request": request, "data": data})
