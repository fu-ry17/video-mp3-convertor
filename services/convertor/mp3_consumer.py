import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class Mp3Consumer:
    async def convert_to_mp3(self, message):
        logger.info(f"Convert to mp3 {message}")
        pass


mp3_consumer_events = {
    "upload.file": Mp3Consumer().convert_to_mp3
}
