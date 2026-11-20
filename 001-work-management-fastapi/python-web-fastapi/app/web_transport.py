"""HTTP contracts for generated browser and JSON clients."""
import json
import math
from pathlib import Path
from urllib.parse import quote

from fastapi import HTTPException, Response
from fastapi.responses import FileResponse, HTMLResponse, JSONResponse, RedirectResponse

FRONTEND = Path(__file__).resolve().parents[1] / "frontend"


def api_request(request):
    return request.url.path.startswith("/api/")


def destination(request, path):
    if api_request(request):
        return JSONResponse({"location": path}, headers={"Cache-Control": "no-store"})
    return RedirectResponse(path, status_code=303)


async def body(request, media_type):
    origin = request.headers.get("origin")
    if origin is not None and origin != str(request.base_url).rstrip("/"):
        raise HTTPException(403, "Invalid request origin")
    if request.headers.get("content-type", "").partition(";")[0].strip().lower() != media_type:
        raise HTTPException(415, f"Expected {media_type}")
    result = bytearray()
    async for chunk in request.stream():
        if len(result) + len(chunk) > 8192:
            raise HTTPException(413, "Request body is too large")
        result.extend(chunk)
    return result


async def json_fields(request, allowed):
    payload = await body(request, "application/json")
    try:
        data = json.loads(payload)
    except (ValueError, RecursionError) as error:
        raise HTTPException(400, "Invalid JSON") from error
    if not isinstance(data, dict) or set(data).difference(allowed):
        raise HTTPException(400, "Expected an object containing only declared fields")
    if any(isinstance(value, (list, dict)) for value in data.values()):
        raise HTTPException(400, "Expected scalar field values")
    if any(isinstance(value, float) and not math.isfinite(value) for value in data.values()):
        raise HTTPException(400, "Expected finite numeric values")
    return data


def browser_shell(request):
    if getattr(request.app.state, "react_ui", False) and not api_request(request) and "text/html" in request.headers.get("accept", ""):
        # The browser fetches the view as JSON before the module mounts React.
        # Only the same-origin URL is interpolated into the static document.
        url = "/api" + quote(request.url.path, safe="/")
        html = (FRONTEND / "index.html").read_text(encoding="utf-8").replace("__TEAQL_VIEW_URL__", url)
        return HTMLResponse(html, headers={"Cache-Control": "no-store", "Vary": "Accept"})


def private_response(response: Response):
    response.headers["Cache-Control"] = "no-store"


def install_frontend(app):
    app.state.react_ui = True

    @app.get("/_teaql/app.js", include_in_schema=False)
    async def javascript():
        return FileResponse(FRONTEND / "dist/app.js", media_type="application/javascript")

    @app.get("/_teaql/base.css", include_in_schema=False)
    async def stylesheet():
        return FileResponse(FRONTEND / "base.css", media_type="text/css")
