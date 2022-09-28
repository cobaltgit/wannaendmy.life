import json
from pathlib import Path

from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

__all__ = ("app", "views")

_dirname = Path(__file__).parent.absolute()

app = FastAPI(
    name="Suicide Prevention Hotlink",
    description="This app serves as a redirect to your national suicide prevention helpline through GeoIP",
    redoc_url=None,
)

app.mount("/static", StaticFiles(directory=_dirname / "static"), name="static")

app.templates = Jinja2Templates(directory=_dirname / "templates")

app.hotlines = json.loads((_dirname / "countries.json").read_text())

from app import views

del _dirname, json, FastAPI, StaticFiles, Jinja2Templates, Path
