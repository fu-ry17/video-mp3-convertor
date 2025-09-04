from fastapi import APIRouter, Depends
from sqlmodel.ext.asyncio.session import AsyncSession

from src.db.main import get_session

from .schema import LoginSchema, RegisterSchema
from .service import AuthService
from .depenencies import AccessTokenBearer

auth_router = APIRouter()
auth_service = AuthService()
access_token_bearer = AccessTokenBearer()

@auth_router.post('/sign-in')
async def login(data: LoginSchema, session: AsyncSession = Depends(get_session)):
    return await auth_service.login_user(data, session)

@auth_router.post('/sign-up')
async def register(data: RegisterSchema, session: AsyncSession = Depends(get_session)):
    return await auth_service.create_user(data, session)

@auth_router.get('/verify')
async def verify(token_data: dict = Depends(access_token_bearer)):
    return token_data
