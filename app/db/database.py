from typing import AsyncGenerator

from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine
from sqlalchemy.ext.asyncio.session import AsyncSession
from sqlalchemy.orm import DeclarativeBase

from app.core.config import settings


async_engine = create_async_engine(settings.ASYNC_DATABASE_URL)
async_session_maker = async_sessionmaker(async_engine, class_=AsyncSession)


class Base(DeclarativeBase):
    pass


async def get_db() -> AsyncGenerator:
    async with async_session_maker() as session:
        yield session
