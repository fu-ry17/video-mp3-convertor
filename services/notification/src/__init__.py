from contextlib import asynccontextmanager
from fastapi import FastAPI

from src.consumer import user_consumer
from src.rabbitmq import rabbitmq

CONSUMERS = user_consumer.user_events

@asynccontextmanager
async def life_span(app: FastAPI):
    await rabbitmq.connect()

    for queue, handler in CONSUMERS.items():
      await rabbitmq.consume(queue, handler)

    yield
    await rabbitmq.disconnect()


app = FastAPI(
    title="notification",
    description="notification service",
    lifespan=life_span
)
