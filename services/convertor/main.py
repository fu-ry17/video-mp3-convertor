from contextlib import asynccontextmanager
from fastapi import FastAPI
from rabbitmq import rabbitmq
import mp3_consumer

CONSUMERS = mp3_consumer.mp3_consumer_events

@asynccontextmanager
async def life_span(app: FastAPI):
    await rabbitmq.connect()

    for queue, handler in CONSUMERS.items():
      await rabbitmq.consume(queue, handler)

    yield
    await rabbitmq.disconnect()


app = FastAPI(
    title="convertor",
    description="Convertor service",
    lifespan=life_span
)

@app.get("/health")
async def health():
    return { "status": "ok" }
