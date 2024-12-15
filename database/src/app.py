import asyncio
from contextlib import asynccontextmanager
from typing import AsyncGenerator

import aio_pika
import uvicorn
from fastapi import FastAPI

from src.handlers import (add_meme, change_visibility, delete_meme, list_saved,
                          meme_saves, random_meme, rate_meme)
from src.storage.rabbitmq import channel_pool


async def process_messages():
    async with channel_pool.acquire() as channel: # type: aio_pika.Channel
        exchange = await channel.declare_exchange('meme_exchange', aio_pika.ExchangeType.DIRECT)
        add_meme_queue = await channel.declare_queue('add_meme_queue', durable=True)
        await add_meme_queue.bind(exchange, routing_key='add_meme')
        await add_meme_queue.consume(add_meme.add_meme)
        random_meme_queue = await channel.declare_queue('random_meme_queue', durable=True)
        await random_meme_queue.bind(exchange, routing_key='random_meme')
        await random_meme_queue.consume(random_meme.random_meme)
        rate_meme_queue = await channel.declare_queue('rate_meme_queue', durable=True)
        await rate_meme_queue.bind(exchange, routing_key='rate_meme')
        await rate_meme_queue.consume(rate_meme.rate_meme)
        remove_rating_queue = await channel.declare_queue('remove_rating_queue', durable=True)
        await remove_rating_queue.bind(exchange, routing_key='remove_rating')
        await remove_rating_queue.consume(rate_meme.remove_rating)
        add_saved_queue = await channel.declare_queue('add_saved_queue', durable=True)
        await add_saved_queue.bind(exchange, routing_key='add_to_saved')
        await add_saved_queue.consume(meme_saves.add_to_saved)
        remove_saved_queue = await channel.declare_queue('remove_saved_queue', durable=True)
        await remove_saved_queue.bind(exchange, routing_key='remove_from_saved')
        await remove_saved_queue.consume(meme_saves.remove_from_saved)
        change_visibility_queue = await channel.declare_queue('change_visibility_queue', durable=True)
        await change_visibility_queue.bind(exchange, routing_key='change_visibility')
        await change_visibility_queue.consume(change_visibility.change_visibility)
        delete_meme_queue = await channel.declare_queue('delete_meme_queue', durable=True)
        await delete_meme_queue.bind(exchange, routing_key='delete_meme')
        await delete_meme_queue.consume(delete_meme.delete_meme)
        first_saved_meme_queue = await channel.declare_queue('first_saved_meme_queue', durable=True)
        await first_saved_meme_queue.bind(exchange, routing_key='first_saved')
        await first_saved_meme_queue.consume(list_saved.first_meme)
        get_saved_meme_queue = await channel.declare_queue('get_saved_meme_queue', durable=True)
        await get_saved_meme_queue.bind(exchange, routing_key='get_saved')
        await get_saved_meme_queue.consume(list_saved.get_meme)


@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncGenerator[None, None]:
    task = asyncio.create_task(process_messages())
    yield
    task.cancel()


def create_app() -> FastAPI:
    return FastAPI(docs_url='/swagger', lifespan=lifespan)


if __name__ == '__main__':
    uvicorn.run(
        'src.app:create_app',
        factory=True,
        host='127.0.0.1',
        port=8001,
        workers=1,
    )
