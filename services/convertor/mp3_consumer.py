import pathlib
import shutil
from bson import ObjectId
import logging, gridfs, os, subprocess
import uuid
from pymongo import MongoClient
import httpx

from rabbitmq import rabbitmq

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

mongo_video = MongoClient(os.getenv("MONGODB_URL"))["videos"]
mongo_mp3 = MongoClient(os.getenv("MONGODB_URL"))["mp3s"]

fs_videos = gridfs.GridFS(mongo_video)
fs_mp3s = gridfs.GridFS(mongo_mp3)

MEDIA_URL = os.getenv("MEDIA_URL")

class Mp3Consumer:
    def __init__(self):
        self.client = httpx.AsyncClient()

    async def convert_to_mp3(self, message):
        logger.info(f"Convert to mp3 {message}")

        base_dir = pathlib.Path("/tmp") / str(uuid.uuid4())
        base_dir.mkdir(parents=True, exist_ok=True)

        try:
            video_file = fs_videos.get(ObjectId(message['video_id']))

            temp_video_path = base_dir / f"{uuid.uuid4()}.mp4"
            output_path = base_dir / f"{uuid.uuid4()}.mp3"

            # Save video to temp file
            with open(temp_video_path, "wb") as f:
                f.write(video_file.read())

            convert_cmd = f"ffmpeg -i {temp_video_path} -vn -ar 44100 -ac 2 -b:a 192k {output_path}"
            subprocess.run(convert_cmd, shell=True, check=True, capture_output=True)

            # Save mp3 to GridFS
            with open(output_path, "rb") as f:
                file_id = fs_mp3s.put(f)

            body = {
                "username": message['username'],
                "status": "processed",
                "mp3_id": str(file_id)
            }

            await self.client.patch(f"{MEDIA_URL}/user/media/{message['video_id']}", json=body)

            # Send RabbitMQ payload
            payload = {
                "video_id": None,
                "mp3_id": str(file_id),
                "username": message['username'],
            }

            await rabbitmq.send_message("upload.converted", payload)

            logger.info(f"Successfully converted video {video_file._id} → mp3 {file_id}")

            if base_dir.exists():
                shutil.rmtree(base_dir, ignore_errors=True)

        except Exception as e:
            logger.error(f"Failed to convert to mp3: {e}", exc_info=True)
            body = {
                "username": message['username'],
                "status": "failed",
                "mp3_id": None
            }

            await self.client.patch(f"{MEDIA_URL}/user/media/{message['video_id']}", json=body)
            if base_dir.exists():
                shutil.rmtree(base_dir, ignore_errors=True)


mp3_consumer_events = {
    "upload.file": Mp3Consumer().convert_to_mp3
}
