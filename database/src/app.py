import asyncio
from typing import AsyncGenerator

from contextlib import asynccontextmanager
from fastapi import FastAPI
import aio_pika
import uvicorn

from src.storage.rabbitmq import channel_pool
from src.handlers.add_meme import add_meme

async def process_messages():
    async with channel_pool.acquire() as channel:
        channel: aio_pika.Channel
        exchange = await channel.declare_exchange('meme_exchange', aio_pika.ExchangeType.DIRECT)
        add_meme_queue = await channel.declare_queue('add_meme_queue', durable=True)
        await add_meme_queue.bind(exchange, routing_key='add_meme')
        await add_meme_queue.consume(add_meme)


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
