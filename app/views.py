import aiohttp
from fastapi import HTTPException, Request
from fastapi.responses import JSONResponse
from starlette.templating import _TemplateResponse

from app import app


@app.get("/")
async def root(request: Request) -> _TemplateResponse:
    async with aiohttp.ClientSession() as cs:
        if ip := request.client.host == "127.0.0.1":
            async with cs.get("https://api.ipify.org") as pub_ip:
                ip = await pub_ip.text()
        async with cs.get(f"https://ipinfo.io/{ip.strip()}/country") as rq:
            code = (await rq.text()).strip()
            info = app.hotlines[code]
            return app.templates.TemplateResponse(
                "index.html",
                {
                    "request": request,
                    "country": code,
                    "number": info.get("number"),
                    "website": info.get("website"),
                    "alt": info.get("alt"),
                },
            )


@app.get("/{code}")
async def code(code: str) -> JSONResponse:
    code = code.upper()
    if code in app.hotlines and len(code) == 2:
        return app.hotlines[code]
    else:
        raise HTTPException(
            status_code=404,
            detail="This country code is not in our database. Please ensure that the provided code exists as a country code and has a length of two characters.",
        )
