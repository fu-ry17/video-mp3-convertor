from fastapi import APIRouter, UploadFile, Depends
from .schema import MediaUpdateRequest

from .service import MediaService
from src.auth import AuthBearer

media_router = APIRouter()
media_service = MediaService()
authBearer = AuthBearer()

@media_router.post("/upload")
async def upload(file: UploadFile, user: dict = Depends(authBearer)):
    return await media_service.upload_videos(user, file)

@media_router.get("/download/{fid}")
async def download(fid: str, _: dict = Depends(authBearer)):
    return await media_service.download_video(fid)

@media_router.get("/user/media")
async def get_user_media(user: dict = Depends(authBearer)):
    return await media_service.get_user_media(user["user_id"])

@media_router.patch("/user/media/{video_id}")
async def update_user_media(video_id: str, payload: MediaUpdateRequest):
    return await media_service.update_user_media(video_id, payload)
