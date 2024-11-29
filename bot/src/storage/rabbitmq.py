import asyncio
import uuid

import msgpack
import aio_pika
from aio_pika.abc import AbstractRobustConnection
from aio_pika.pool import Pool

from config.settings import settings


async def get_connection() -> AbstractRobustConnection:
    return await aio_pika.connect_robust(settings.rabbit_url)


connection_pool: Pool = Pool(get_connection, max_size=2)


async def get_channel() -> aio_pika.Channel:
    async with connection_pool.acquire() as connection:
        return await connection.channel()


channel_pool: Pool = Pool(get_channel, max_size=10)


async def publish_message(routing_key: str, message: dict):
    async with channel_pool.acquire() as channel:
        exchange = await channel.declare_exchange('meme_exchange', aio_pika.ExchangeType.DIRECT)
        await exchange.publish(
            aio_pika.Message(
                body=msgpack.packb(message),
                delivery_mode=aio_pika.DeliveryMode.PERSISTENT,
            ),
            routing_key=routing_key,
        )


async def publish_message_with_response(routing_key: str, message: dict) -> asyncio.Future:
    response = {}
    async with channel_pool.acquire() as channel:
        channel: aio_pika.Channel
        exchange = await channel.declare_exchange('meme_exchange', aio_pika.ExchangeType.DIRECT)
        callback_queue = await channel.declare_queue(exclusive=True)
        await callback_queue.bind(exchange, routing_key=callback_queue.name)
        correlation_id = str(uuid.uuid4())
        future_response = asyncio.Future()

        async def on_response(message: aio_pika.IncomingMessage):
            if message.correlation_id == correlation_id:
                future_response.set_result(msgpack.unpackb(message.body))

        await callback_queue.consume(on_response)
        await exchange.publish(
            aio_pika.Message(
                body=msgpack.packb(message),
                reply_to=str(callback_queue.name),
                correlation_id=correlation_id,
            ),
            routing_key=routing_key,
        )
        response = await future_response
        await callback_queue.delete(if_unused=False, if_empty=False)
        return response
