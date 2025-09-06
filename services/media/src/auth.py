from fastapi import HTTPException, Request
from fastapi.security import HTTPBearer
import httpx, os

AUTH_URL = os.environ.get("AUTH_URL")

class AuthBearer(HTTPBearer):
    def __init__(self, auto_error: bool = True):
        super().__init__(auto_error=auto_error)

    async def __call__(self, request: Request):
       creds = await super().__call__(request)
       if not creds:
           raise HTTPException(status_code=401, detail="Missing credentials")
       return await self.verify(creds.credentials)

    async def verify(self, token):
        async with httpx.AsyncClient() as client:
            response = await client.get(f"{AUTH_URL}/verify", headers={"Authorization": f"Bearer {token}"})
            if response.status_code != 200:
                raise HTTPException(status_code=401, detail="Invalid token")

            return response.json()['user']
