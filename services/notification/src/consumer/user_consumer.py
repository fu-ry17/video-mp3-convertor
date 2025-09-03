import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class UserConsumer:
    async def send_welcome_email(self, message):
        logger.info({ "message": message })
        # logger.info(f"Sending welcome email, {message.email}")


user_events = {
    "user.created": UserConsumer().send_welcome_email,
    "user.login": UserConsumer().send_welcome_email,
}
