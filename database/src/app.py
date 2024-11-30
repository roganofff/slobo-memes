import asyncio
from typing import AsyncGenerator

from contextlib import asynccontextmanager
from fastapi import FastAPI
import aio_pika
import uvicorn

from src.storage.rabbitmq import channel_pool
from src.handlers import add_meme, random_meme, rate_meme

async def process_messages():
    async with channel_pool.acquire() as channel:
        channel: aio_pika.Channel
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


@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncGenerator[None, None]:
    task = asyncio.create_task(process_messages())
    yield
    task.cancel()


def create_app() -> FastAPI:
    app = FastAPI(docs_url='/swagger', lifespan=lifespan)
    return app


if __name__ == '__main__':
    uvicorn.run(
        'src.app:create_app',
        factory=True,
        host='0.0.0.0',
        port=8001,
        workers=1,
    )
