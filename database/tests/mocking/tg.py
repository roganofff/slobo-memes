from aio_pika import IncomingMessage
from aiogram.types import User, Chat
from unittest.mock import AsyncMock


class MockTgMessage(IncomingMessage):
    ...