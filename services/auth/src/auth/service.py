from datetime import timedelta
from fastapi import status
from fastapi.exceptions import HTTPException
from fastapi.responses import JSONResponse
from sqlmodel import select
from sqlmodel.ext.asyncio.session import AsyncSession


from src.rabbitmq import rabbitmq
from src.auth import utils
from src.db.models import User
from .schema import RegisterSchema, LoginSchema


class AuthService:
    async def get_user_by_email(self, email: str, session: AsyncSession):
        statement = select(User).where(User.email == email)
        result = await session.exec(statement)
        return result.first()

    async def user_exists(self, email: str, session: AsyncSession) -> bool:
        user = await self.get_user_by_email(email, session)
        return user is not None

    async def create_user(self, data: RegisterSchema, session: AsyncSession):
        if await self.user_exists(data.email, session):
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Account already exists")

        # hash_password
        pass_hash = utils.hash_password(data.password)

        # create userimport utils
        new_user = User(**data.model_dump())
        new_user.password_hash = pass_hash

        session.add(new_user)
        await session.commit()

        # send welcome email
        await rabbitmq.send_message('user.created', { 'email': new_user.email })

        return "Registration successful..."

    async def login_user(self, data: LoginSchema, session: AsyncSession):
        user = await self.get_user_by_email(data.email, session)
        if user is not None:
            if utils.compare_password(data.password, user.password_hash):
                # generate tokens
                user_data = { 'user_id': str(user.id) }
                access_token = utils.generate_token(user_data, exp=timedelta(hours=1))
                refresh_token = utils.generate_token(user_data, exp=timedelta(days=2))

                return JSONResponse(
                    content={
                        'access-token': access_token,
                        'refresh-token': refresh_token
                    }
                )

        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials")
