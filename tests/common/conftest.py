from typing import AsyncGenerator
from fastapi import FastAPI
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker
from database.src.storage.database import engine, get_db
import pytest_asyncio


@pytest_asyncio.fixture()
async def db_session(app: FastAPI) -> AsyncGenerator[AsyncSession, None]:
    async with engine.begin() as conn:  # start transaction
        session_maker = async_sessionmaker(bind=conn, class_=AsyncSession)  # create sessio_maker through transcation

        async with session_maker() as session:
            async def overrided_db_session() -> AsyncGenerator[AsyncSession, None]:
                yield session

            app.dependency_overrides[get_db] = overrided_db_session

            yield session
        await conn.rollback()