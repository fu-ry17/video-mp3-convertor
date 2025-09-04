import logging

from src.mail import create_message, mail

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class UserConsumer:
    async def send_welcome_email(self, message):
        logger.info({ "message": message })

        html = f"""
            <h1 style="color:#4CAF50;">👋 Welcome to Video to MP3 Converter!</h1>
            <p>
                Hello <strong>{message['email']}</strong>,
            </p>
            <p>
                We're excited to have you on board. With our service, you can easily convert your favorite videos into high-quality
                MP3 audio files — fast and hassle-free.
            </p>
            <p>
                To get started, simply upload a video and let us handle the rest. 🎶
            </p>
            <hr/>
            <p style="font-size: 12px; color: #666;">
                If you did not sign up for this service, you can safely ignore this email.
            </p>
        """


        mail_message = create_message(
            body=html,
            recipients=[message['username']],
            subject="Welcome to video to mp3 convertor"
        )

        await mail.send_message(mail_message)
        logger.info("Welcome mail sent!")


user_events = {
    "user.created": UserConsumer().send_welcome_email,
}
