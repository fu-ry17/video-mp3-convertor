from fastapi import APIRouter, Depends
from sqlmodel.ext.asyncio.session import AsyncSession

from src.db.main import get_session

from .schema import LoginSchema, RegisterSchema
from .service import AuthService

auth_router = APIRouter()
auth_service = AuthService()

@auth_router.post('/sign-in')
async def login(data: LoginSchema, session: AsyncSession = Depends(get_session)):
    return await auth_service.login_user(data, session)

@auth_router.post('/sign-up')
async def register(data: RegisterSchema, session: AsyncSession = Depends(get_session)):
    return await auth_service.create_user(data, session)
