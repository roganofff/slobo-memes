import uuid
from collections import deque

import aio_pika
import msgpack
import pytest

from src.services.meme import MemeService
from tests.mocking.rabbit import (MockChannel, MockChannelPool, MockExchange,
                                  MockQueue)


@pytest.mark.asyncio()
async def test_handle_meme(mock_exchange: MockExchange) -> None:
    expected_routing_key = 'random_meme'

    mock_queue = MockQueue(deque())
    mock_channel = MockChannel(queue=mock_queue, exchange=mock_exchange)
    mock_pool = MockChannelPool(channel=mock_channel)

    expected_calls = []
    async with mock_pool.acquire() as channel:
        exchange = await channel.declare_exchange('meme_exchange', aio_pika.ExchangeType.DIRECT)
        callback_queue = await channel.declare_queue(exclusive=True)
        await callback_queue.bind(exchange, routing_key=callback_queue.name)
        meme = await MemeService.add_meme(creator_id=1, description='ccc', image_url='ccc')

        expected_message = aio_pika.Message(
            msgpack.packb(meme),
            correlation_id=str(uuid.uuid4()),
        )

        expected_calls.append(
            ('publish', (expected_message,), {'routing_key': expected_routing_key}),
        )

        mock_exchange.assert_has_calls(expected_calls, any_order=True)
