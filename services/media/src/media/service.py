import logging
import os, uuid
from fastapi import HTTPException, UploadFile, status
from fastapi.responses import JSONResponse
import gridfs
from pymongo import MongoClient

from src.rabbitmq import rabbitmq

mongo_video = MongoClient(os.getenv("MONGODB_URL"))["videos"]
mongo_mp3 = MongoClient(os.getenv("MONGODB_URL"))["mp3s"]

fs_videos = gridfs.GridFS(mongo_video)
fs_mp3s = gridfs.GridFS(mongo_mp3)


class MediaService:
    async def upload_videos(self, email: str, file: UploadFile):
        try:
            file_id = fs_videos.put(file.file)

            payload = {
                'video_id': str(file_id),
                'mp3_id': None,
                'username': 'furybrian175@gmail.com' # hardcode for testing
            }

            await rabbitmq.send_message("upload.file", payload)

            return "file uploaded for processing"

        except Exception as e:
            logging.error(f"Failed to upload file: {e}", exc_info=True)
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="An error occured during file upload")


    async def download_video(self):
        pass
