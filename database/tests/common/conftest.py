from collections import deque
from typing import AsyncGenerator
import aio_pika
from fastapi import FastAPI
import msgpack
import pytest
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker
from src.storage import rabbitmq, database
from tests.mocking.rabbit import MockChannel, MockChannelPool, MockExchange, MockExchangeMessage, MockQueue
from src.storage.database import engine, get_db
import pytest_asyncio


@pytest_asyncio.fixture()
async def db_session(app: FastAPI, monkeypatch: pytest.MonkeyPatch) -> AsyncGenerator[AsyncSession, None]:
    async with engine.begin() as conn:  # start transaction
        session_maker = async_sessionmaker(bind=conn, class_=AsyncSession)  # create sessio_maker through transcation

        async with session_maker() as session:
            async def overrided_db_session() -> AsyncGenerator[AsyncSession, None]:
                yield session

            monkeypatch.setattr(database, 'async_session', session_maker)
            app.dependency_overrides[get_db] = overrided_db_session

            yield session
        await conn.rollback()

        
@pytest.fixture()
def mock_exchange() -> MockExchange:
    return MockExchange()


@pytest_asyncio.fixture()
async def load_queue(monkeypatch: pytest.MonkeyPatch, mock_exchange: MockExchange):

    queue = MockQueue(deque())

    channel = MockChannel(queue=queue, exchange=mock_exchange)
    pool = MockChannelPool(channel=channel)
    monkeypatch.setattr(rabbitmq, 'channel_pool', pool)
    monkeypatch.setattr(aio_pika, 'Message', MockExchangeMessage)