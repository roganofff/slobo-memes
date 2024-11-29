import asyncio
import uvicorn

from contextlib import asynccontextmanager
from fastapi import FastAPI
from typing import AsyncGenerator
from aiogram import Dispatcher, Bot, types
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from starlette_context import plugins
from starlette_context.middleware import RawContextMiddleware

from config.settings import settings
from src.bot import setup_dp, setup_bot
from src.background_tasks import background_tasks
from src.api import router as api_router
from src.handlers import router as bot_router
from src.middlewares import chat_action, state

import logging

logging.basicConfig(level=logging.INFO)


async def setup_app() -> tuple[Dispatcher, Bot]:
    # storage = RedisStorage(redis=redis.setup_redis())
    dp = Dispatcher(storage=None)
    setup_dp(dp)
    dp.include_router(bot_router)
    dp.message.middleware(state.StateMiddleware())
    dp.callback_query.middleware(state.StateMiddleware())
    dp.message.middleware(chat_action.ChatActionMiddleware())
    dp.callback_query.middleware(chat_action.ChatActionMiddleware())
    default = DefaultBotProperties(parse_mode=ParseMode.HTML)
    bot = Bot(token=settings.BOT_TOKEN, default=default)
    await bot.set_my_commands(
        [
            types.BotCommand(command='start', description='Перезапустить бота')
        ],
        scope=types.BotCommandScopeAllPrivateChats(),
    )
    setup_bot(bot)
    return dp, bot


@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncGenerator[None, None]:
    _dp, bot = await setup_app()
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
    dp, bot = await setup_app()
    await bot.delete_webhook()
    await dp.start_polling(bot)


if __name__ == '__main__':
    if settings.BOT_FASTAPI_HOST:
        uvicorn.run(
            'src.app:create_app',
            factory=True,
            host='0.0.0.0',
            port=settings.BOT_FASTAPI_PORT,
            workers=1,
        )
    else:
        asyncio.run(start_polling())
