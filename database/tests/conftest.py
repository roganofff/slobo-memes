from typing import AsyncGenerator
from asgi_lifespan import LifespanManager
from fastapi import FastAPI
from src.app import create_app
import pytest
import pytest_asyncio

from httpx import AsyncClient
from alembic import command
from alembic.config import Config
from src.models.meta import Base
from config import settings
from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine, AsyncSession, AsyncEngine


@pytest_asyncio.fixture(scope='session')
async def db_engine() -> AsyncGenerator[AsyncEngine, None]:
    engine = create_async_engine(settings.db_url)

    alembic_cfg = Config('alembic.ini')

    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
        command.upgrade(alembic_cfg, 'head')

    yield engine
    
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
    await engine.dispose()


@pytest_asyncio.fixture
async def db_session(db_engine):
    Session = async_sessionmaker(bind=db_engine, class_=AsyncSession)
    async with Session() as session:
        yield session
