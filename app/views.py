import aiohttp
from fastapi import HTTPException, Request
from fastapi.responses import JSONResponse
from starlette.templating import _TemplateResponse

from app import api, hotlines, utils


@api.get("/")
async def root(request: Request) -> _TemplateResponse:
    code = await utils.get_code(request.client.host)
    info = hotlines[code]
    return api.templates.TemplateResponse(
        "index.html",
        {
            "request": request,
            "country": code,
            "number": info.get("number"),
            "website": info.get("website"),
            "alt": info.get("alt"),
        },
    )


@api.get("/{code}")
async def code(code: str) -> JSONResponse:
    code = code.upper()
    if entry := hotlines.get(code) and len(entry) == 2:
        return entry
    else:
        raise HTTPException(
            status_code=404,
            detail="This country code is not in our database. Please ensure that the provided code exists as a country code and has a length of two characters.",
        )
