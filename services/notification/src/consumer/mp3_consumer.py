import logging
from src.mail import create_message, mail

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class Mp3Consumer:
    async def send_upload_email(self, message):
        logger.info({ "message": message })

        html = f"""
           <h2>Your video has been successfully converted to MP3 🎉</h2>
           <p>
               Your file is ready!<br/>
               <strong>MP3 ID:</strong> {message['mp3_id']}
           </p>
           <p>
               You can now download your converted audio file from your dashboard.
           </p>
           <hr/>
           <p style="font-size: 12px; color: #666;">
               Thank you for using our Video to MP3 Converter.<br/>
               If you didn’t request this conversion, please ignore this email.
           </p>
       """

        mail_message = create_message(
            body=html,
            recipients=[message['username']],
            subject="Video processed!"
        )

        await mail.send_message(mail_message)
        logger.info("Video processed!")


mp3_events = {
    "upload.converted": Mp3Consumer().send_upload_email,
}
