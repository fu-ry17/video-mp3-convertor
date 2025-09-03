import json
import logging
import aio_pika

from src.settings import settings

class RabbitMQ:
    def __init__(self, url: str = settings.RABBITMQ_URL):
        self.url = url
        self.connection = None
        self.channel = None

    async def connect(self):
        self.connection = await aio_pika.connect(self.url)
        self.channel = await self.connection.channel()
        logging.info("Connected to rabbitmq")

    async def disconnect(self):
        if self.connection and not self.connection.is_closed:
            await self.connection.close()
            logging.info("Connected to rabbitmq")

    async def send_message(self, queue_name: str, message: dict):
        if self.channel is not None:
            await self.channel.declare_queue(queue_name, durable=True)

            await self.channel.default_exchange.publish(
                aio_pika.Message(
                    json.dumps(message).encode(),
                    delivery_mode=aio_pika.DeliveryMode.PERSISTENT
                ),
                routing_key=queue_name
            )

rabbitmq = RabbitMQ()
