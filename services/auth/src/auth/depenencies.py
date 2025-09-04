from typing_extensions import Required
from fastapi import HTTPException, Request
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from .utils import decode

class TokenBearer(HTTPBearer):
    def __init__(self, auto_error: bool = True):
        super().__init__(auto_error=auto_error)

    async def __call__(self, request: Request) -> HTTPAuthorizationCredentials | None:
        creds = await super().__call__(request)
        token = creds.credentials

        if not token:
            raise HTTPException(status_code=401, detail="Unauthorized access")

        token_data = decode(token)

        if not await self.is_valid(token):
            raise HTTPException(status_code=401, detail="Invalid token")

        self.verify_token_data(token_data)

        return token_data

    async def is_valid(self, token: str) -> bool:
        token_data = decode(token)
        return token_data is not None

    def verify_token_data(self, token_data):
        raise NotImplementedError("Please Override this method in child classes")


class AccessTokenBearer(TokenBearer):
    def verify_token_data(self, token_data: dict) -> None:
        if token_data and token_data["refresh"]:
            raise HTTPException(status_code=401, detail="Invalid access token")

class RefreshTokenBearer(TokenBearer):
    def verify_token_data(self, token_data: dict) -> None:
        if token_data and not token_data["refresh"]:
            raise HTTPException(status_code=401, detail="Invalid refresh token")
