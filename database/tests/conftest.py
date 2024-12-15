from typing import AsyncGenerator

import pytest_asyncio
from sqlalchemy.ext.asyncio import (AsyncEngine, AsyncSession,
                                    async_sessionmaker, create_async_engine)

from alembic import command
from alembic.config import Config
from config import settings
from src.models.meta import Base


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
