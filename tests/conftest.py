from typing import AsyncGenerator
from asgi_lifespan import LifespanManager
from fastapi import FastAPI
from bot.src.app import create_app
import pytest
import pytest_asyncio

from httpx import AsyncClient
from alembic import command
from alembic.config import Config
from database.src.models.meta import Base
from tests.config import settings
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


@pytest.fixture(scope='session')
def app() -> FastAPI:
    return create_app()


@pytest_asyncio.fixture
async def test_client() -> AsyncGenerator[AsyncEngine, None]:
    async with LifespanManager(app):
        async with AsyncClient(app=app, base_url='http://localhost') as client:
            yield client
