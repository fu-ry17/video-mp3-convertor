from fastapi.exceptions import HTTPException
import os, httpx
from fastapi import FastAPI, Request, status
from starlette.responses import Response

SERVICES = {
    "auth": os.getenv("AUTH_URL", "http://localhost:5000"),
    "media": os.getenv("MEDIA_URL", "http://localhost:7000")
}

app = FastAPI(
    redoc_url=None,
    docs_url=None,
)

async def check_service_health(url: str):
    health_url = f"{url}/health"
    try:
        async with httpx.AsyncClient(timeout=3) as client:
            resp = await client.get(health_url)
            if resp.status_code == 200:
                return "up"
            else:
                return "down"
    except Exception:
        return "down"


@app.get("/health")
async def health():
    return { "status": "ok" }

@app.get("/")
async def root():
    services_status = {}
    for service, url in SERVICES.items():
        status = await check_service_health(url)
        services_status[service] = {
            "url": url,
            "docs": f"{url}/docs",
            "prefix": f"/api/{service}/:paths",
            "status": status
        }

    return {
        "message": "Welcome to Video MP3 Convertor Services",
        "services": services_status
    }


@app.api_route("/api/{service}", methods=["GET", "PUT", "POST", "DELETE", "PATCH", "OPTIONS", "HEADER"])
async def proxy_root(service: str, request: Request):
    base = SERVICES.get(service)
    if not base:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Service not found")

    return await _proxy(request, base, "")

@app.api_route("/api/{service}/{path:path}", methods=["GET", "PUT", "POST", "DELETE", "PATCH", "OPTIONS", "HEADER"])
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
