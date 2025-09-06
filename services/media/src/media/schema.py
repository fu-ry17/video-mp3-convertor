from pydantic import BaseModel
from typing import Optional

class MediaUpdateRequest(BaseModel):
    username: str
    status: str
    mp3_id: Optional[str] = None
