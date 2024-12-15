import uuid
from collections import deque
from typing import Any
from unittest.mock import AsyncMock

import aio_pika
import msgpack
import pytest

from src import bot
from tests.mocking.rabbit import (MockChannel, MockChannelPool, MockExchange,
                                  MockQueue)


@pytest.fixture(autouse=True)
def mock_bot_dp(monkeypatch: pytest.MonkeyPatch) -> AsyncMock:
    mock = AsyncMock()
    monkeypatch.setattr(bot, 'get_dp', mock)
    return mock


@pytest.fixture()
def mock_exchange() -> MockExchange:
    return MockExchange()


@pytest.fixture()
def mock_channel_pool(mock_exchange) -> MockChannelPool:
    queue = MockQueue(deque())
    channel = MockChannel(queue=queue, exchange=mock_exchange)
    return MockChannelPool(channel=channel)


@pytest.fixture
def mock_publish_and_send_methods(
    monkeypatch: pytest.MonkeyPatch,
    mock_channel_pool: MockChannelPool,
) -> None:
    async def mock_publish_message_with_response(routing_key, message) -> dict[str, Any]:
        async with mock_channel_pool.acquire() as channel:
            exchange = await channel.declare_exchange(
                'meme_exchange',
                aio_pika.ExchangeType.DIRECT,
            )
            callback_queue = await channel.declare_queue(exclusive=True)
            await callback_queue.bind(exchange, routing_key=callback_queue.name)

            await exchange.publish(
                aio_pika.Message(
                    body=msgpack.packb(message),
                    correlation_id=str(uuid.uuid4()),
                ),
                routing_key=routing_key,
            )

        return {
            'description': 'Test description',
            'creator_id': 123,
            'is_saved': True,
            'is_public': True,
            'likes': 10,
            'dislikes': 2,
            'user_rating': 5,
            'pagination': [None, None],
            'image_url': 'http://example.com/image.jpg',
            'id': 'test_meme_id',
        }

    monkeypatch.setattr(
        'src.handlers.list_saved.publish_message_with_response',
        mock_publish_message_with_response,
    )

    async def mock_edit_or_send_message(message_args, message_id) -> None:
        return

    monkeypatch.setattr(
        'src.handlers.list_saved.edit_or_send_message',
        mock_edit_or_send_message,
    )
