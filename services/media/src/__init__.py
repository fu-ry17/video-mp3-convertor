from contextlib import asynccontextmanager
from fastapi import FastAPI

from src.rabbitmq import rabbitmq
from src.media.routes import media_router


@asynccontextmanager
async def life_span(app: FastAPI):
    await rabbitmq.connect()
    yield
    await rabbitmq.disconnect()

app = FastAPI(
    title="media service",
    description="handles media upload and download",
    lifespan=life_span
)

@app.get("/health")
async def health():
    return { "status": "ok" }


app.include_router(media_router, tags=["media"])
