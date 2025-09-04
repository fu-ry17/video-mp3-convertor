from fastapi import APIRouter, UploadFile, Depends

from .service import MediaService
from src.auth import AuthBearer

media_router = APIRouter()
media_service = MediaService()
authBearer = AuthBearer()

@media_router.post("/upload")
async def upload(file: UploadFile, user: dict = Depends(authBearer)):
    return await media_service.upload_videos(user["email"], file)

@media_router.get("/download/{fid}")
async def download(fid: str, _: dict = Depends(authBearer)):
    return await media_service.download_video(fid)
