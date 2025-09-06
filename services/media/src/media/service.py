from datetime import datetime
import logging
import os, uuid
from fastapi import HTTPException, UploadFile, status
from fastapi.responses import StreamingResponse
from bson import ObjectId
import gridfs
from pymongo import MongoClient

from .schema import MediaUpdateRequest
from src.rabbitmq import rabbitmq

mongo_video = MongoClient(os.getenv("MONGODB_URL"))["videos"]
mongo_mp3 = MongoClient(os.getenv("MONGODB_URL"))["mp3s"]

media = MongoClient(os.getenv("MONGODB_URL"))["media"]
media_client = media["media"]

fs_videos = gridfs.GridFS(mongo_video)
fs_mp3s = gridfs.GridFS(mongo_mp3)


class MediaService:
    async def upload_videos(self, user: dict, file: UploadFile):
        try:
            file_id = fs_videos.put(file.file)

            logging.info(user)

            doc = {
                'user_id': user['user_id'],
                'video_id': str(file_id),
                'mp3_id': None,
                'username': user['email'],
                'status': 'processing',
                'created_at': datetime.now(),
                'updated_at': datetime.now()
            }

            # insert into media collection
            media_client.insert_one(doc)

            payload = {
                'video_id': str(file_id),
                'mp3_id': None,
                'username': user['email']
            }

            await rabbitmq.send_message("upload.file", payload)

            return "file uploaded for processing"

        except Exception as e:
            print("Error", e)
            logging.error(f"Failed to upload file: {e}", exc_info=True)
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="An error occured during file upload")


    async def download_video(self, fid: str):
        try:
            out = fs_mp3s.get(ObjectId(fid))
            return StreamingResponse(
                out,
                media_type="audio/mpeg",
                headers={"Content-Disposition": f"attachment; filename={fid}.mp3"}
            )
        except Exception as err:
            logging.error(f"Download error: {err}", exc_info=True)
            raise HTTPException(status_code=500, detail="internal server error")

    async def get_user_media(self, user_id: str):
        try:
            media = media_client.find({'user_id': user_id})
            return media
        except Exception as err:
            logging.error(f"Failed to get user media: {err}", exc_info=True)
            raise HTTPException(status_code=500, detail="internal server error")

    async def update_user_media(self, video_id: str, payload: MediaUpdateRequest):
        try:
            result = media_client.update_one(
                {"video_id": video_id},
                {"$set": {"status": payload.status, "mp3_id": payload.mp3_id}}
            )

            if not result.matched_count:
                raise HTTPException(status_code=404, detail="Media not found")

            return {"message": "Media updated"}

        except Exception as err:
            logging.error(f"Failed to update user media: {err}", exc_info=True)
            raise HTTPException(status_code=500, detail="internal server error")
