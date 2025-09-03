from fastapi.exceptions import HTTPException
import os, httpx
from fastapi import FastAPI, Request, status
from starlette.responses import Response

SERVICES = {
    "auth": os.getenv("AUTH_URL", "http://localhost:5000")
}

app = FastAPI(
    redoc_url=None,
    docs_url=None,
)

@app.api_route("/{service}", methods=["GET", "PUT", "POST", "DELETE", "PATCH", "OPTIONS", "HEADER"])
async def proxy_root(service: str, request: Request):
    base = SERVICES.get(service)
    if not base:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Service not found")

    return await _proxy(request, base, "")

@app.api_route("/{service}/{path:path}", methods=["GET", "PUT", "POST", "DELETE", "PATCH", "OPTIONS", "HEADER"])
async def proxy(service: str, path: str, request: Request):
    base = SERVICES.get(service)
    if not base:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Service not found")

    return await _proxy(request, base, path)


async def _proxy(request: Request, base: str, path: str):
    url = f"{base}/{path}" if path else base
    print(url)
    body = await request.body()
    content_type = request.headers.get("content-type")

    try:
       async with httpx.AsyncClient(follow_redirects=False) as client:
           resp = await client.request(
               request.method,
               url,
               params=request.query_params,
               content=body,
               headers= {"content-type": content_type} if content_type else None
           )
    except httpx.RequestError as exc:
        raise HTTPException(status_code=502, detail=f"Upstream error: {exc}") from exc

    return Response(
        content=resp.content,
        status_code=resp.status_code,
        media_type=resp.headers.get("content-type")
    )
