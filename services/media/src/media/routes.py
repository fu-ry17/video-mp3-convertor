from fastapi import APIRouter, UploadFile

from .service import MediaService

media_router = APIRouter()
media_service = MediaService()

@media_router.post("/upload")
async def upload(file: UploadFile):
    return await media_service.upload_videos("furybrian175@gmail.com", file)
