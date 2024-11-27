import asyncio
import uvicorn

from contextlib import asynccontextmanager
from fastapi import FastAPI
from typing import AsyncGenerator
from aiogram import Dispatcher, Bot
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from starlette_context import plugins
from starlette_context.middleware import RawContextMiddleware

from config.settings import settings
from src.bot import setup_dp, setup_bot
from src.background_tasks import background_tasks
from src.api import router as api_router
from src.handlers import router as bot_router

import logging

logging.basicConfig(level=logging.INFO)


@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncGenerator[None, None]:
    dp = Dispatcher()
    setup_dp(dp)
    dp.include_router(bot_router)
    default = DefaultBotProperties(parse_mode=ParseMode.HTML)
    bot = Bot(token=settings.BOT_TOKEN, default=default)
    setup_bot(bot)
    await bot.set_webhook(settings.bot_webhook_url)
    yield
    while background_tasks:
        await asyncio.sleep(0)
    await bot.delete_webhook()


def create_app() -> FastAPI:
    app = FastAPI(docs_url='/swagger', lifespan=lifespan)
    app.include_router(api_router)
    app.add_middleware(RawContextMiddleware, plugins=[plugins.CorrelationIdPlugin()])
    return app


async def start_polling() -> None:
    dp = Dispatcher()
    setup_dp(dp)
    dp.include_router(bot_router)
    default = DefaultBotProperties(parse_mode=ParseMode.HTML)
    bot = Bot(token=settings.BOT_TOKEN, default=default)
    setup_bot(bot)
    await bot.delete_webhook()
    await dp.start_polling(bot)


if __name__ == '__main__':
    if settings.WEBHOOK_URL:
        uvicorn.run('src.app:create_app', factory=True, host='0.0.0.0', port=8000, workers=1)
    else:
        asyncio.run(start_polling())
