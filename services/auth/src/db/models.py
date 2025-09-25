import uuid
from sqlalchemy import func
import sqlalchemy.dialects.postgresql as pg
from sqlmodel import Column, Field, SQLModel
from datetime import datetime

class User(SQLModel, table=True):
    __tablename__ = "mp3_convertor_users"

    id: uuid.UUID = Field(
        sa_column=Column(
            pg.UUID,
            primary_key=True,
            nullable=False,
            default=uuid.uuid4
        )
    )
    username: str
    email: str = Field(index=True) # contantly searched
    password_hash: str = Field(exclude=True)
    created_at: datetime = Field(
        sa_column=Column(
            pg.TIMESTAMP,
            default=func.now(),
            nullable=False
        )
    )
    updated_at: datetime = Field(
        sa_column=Column(
            pg.TIMESTAMP,
            default=func.now(),
            nullable=False
        )
    )
