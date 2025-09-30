from fastapi import APIRouter, Depends
from sqlmodel.ext.asyncio.session import AsyncSession

from src.db.main import get_session

from .schema import LoginSchema, RegisterSchema
from .service import AuthService
from .depenencies import AccessTokenBearer, RefreshTokenBearer

auth_router = APIRouter()
auth_service = AuthService()
access_token_bearer = AccessTokenBearer()
refresh_token_bearer = RefreshTokenBearer()

@auth_router.post('/sign-in')
async def login(data: LoginSchema, session: AsyncSession = Depends(get_session)):
    return await auth_service.login_user(data, session)

@auth_router.post('/sign-up')
async def register(data: RegisterSchema, session: AsyncSession = Depends(get_session)):
    return await auth_service.create_user(data, session)

@auth_router.get('/verify')
async def verify(token_data: dict = Depends(access_token_bearer)):
    return token_data

@auth_router.get('/refresh-token')
async def refresh_token(token_data: dict = Depends(refresh_token_bearer)):
    return await auth_service.refresh_token(token_data)
