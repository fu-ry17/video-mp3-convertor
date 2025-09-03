from contextlib import asynccontextmanager
from fastapi import FastAPI
from src.rabbitmq import rabbitmq
from src.auth.routes import auth_router
from src.db.main import init_db

@asynccontextmanager
async def life_span(app: FastAPI):
    await init_db()
    await rabbitmq.connect()
    yield
    await rabbitmq.disconnect()


prefix = "v1"

app = FastAPI(
    title="auth-service",
    version=prefix,
    lifespan=life_span,
)

@app.get("/health")
async def health():
    return { "status": "ok" }

app.include_router(auth_router, tags=["auth"])
