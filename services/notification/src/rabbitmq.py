import os
import aio_pika, json
from aio_pika.abc import AbstractIncomingMessage

import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class RabbitMQ:
    def __init__(self, url: str = os.getenv("RABBITMQ_URL", "amqp://admin:pass@localhost:5672")):
        self.url = url
        self.connection = None
        self.channel = None

    async def connect(self):
        self.connection = await aio_pika.connect(self.url)
        self.channel = await self.connection.channel()
        logger.info("Connected to rabbitmq...")

    async def disconnect(self):
        if self.connection and self.connection.is_closed:
            await self.connection.close()

    async def send_message(self, queue_name: str, message: dict):
        if self.channel:
            await self.channel.declare_queue(queue_name, durable=True)

            await self.channel.default_exchange.publish(
                message=aio_pika.Message(
                    json.dumps(message).encode(),
                    delivery_mode=aio_pika.DeliveryMode.PERSISTENT
                ),
                routing_key=queue_name
            )

    async def consume(self, queue_name: str, callback):
        if not self.channel:
            raise RuntimeError("RabbitMQ channel is not initialized")

        queue = await self.channel.declare_queue(queue_name, durable=True)

        async def _wrapper(message: AbstractIncomingMessage):
            try:
                payload = json.loads(message.body.decode())
                await callback(payload)
                await message.ack()
                logger.info(f"✅ Acked message from {queue_name}: {payload}")
            except Exception as e:
                logger.error(f"❌ Error handling message from {queue_name}: {e}")
                await message.nack(requeue=True)

        await queue.consume(_wrapper)

rabbitmq = RabbitMQ()
