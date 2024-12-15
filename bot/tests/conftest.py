from typing import AsyncGenerator
from asgi_lifespan import LifespanManager
from fastapi import FastAPI
from httpx import AsyncClient
import pytest
import pytest_asyncio

from src.app import create_app


@pytest.fixture(scope='session')
def app() -> FastAPI:
    return create_app()


@pytest_asyncio.fixture(scope='session')
async def test_client(app: FastAPI) -> AsyncGenerator[AsyncClient, None]:
    async with LifespanManager(app):
        async with AsyncClient(app=app, base_url='http://localhost') as client:
            yield client
