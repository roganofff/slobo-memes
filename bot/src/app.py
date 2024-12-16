import asyncio
import logging
from contextlib import asynccontextmanager
from typing import AsyncGenerator

import uvicorn
from aiogram import Bot, Dispatcher, types
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from fastapi import FastAPI
from starlette_context import plugins
from starlette_context.middleware import RawContextMiddleware

from config.settings import settings
from src.api import router as api_router
from src.background_tasks import background_tasks
from src.bot import setup_bot, setup_dp
from src.handlers import router as bot_router
from src.middlewares import chat_action, state
from src.logger import LOGGING_CONFIG, logger


async def setup_app() -> tuple[Dispatcher, Bot]:
    logging.config.dictConfig(LOGGING_CONFIG)
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
            types.BotCommand(command='start', description='Перезапустить бота'),
        ],
        scope=types.BotCommandScopeAllPrivateChats(),
    )
    setup_bot(bot)
    logger.info('Finished start')
    return dp, bot


@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncGenerator[None, None]:
    _dp, bot = await setup_app()
    await bot.set_webhook(settings.bot_webhook_url)
    yield
    while background_tasks:
        await asyncio.sleep(0)
    await bot.delete_webhook()
    logger.info('Ending lifespan')


def create_app() -> FastAPI:
    app = FastAPI(docs_url='/swagger', lifespan=lifespan)
    app.include_router(api_router)
    app.add_middleware(RawContextMiddleware, plugins=[plugins.CorrelationIdPlugin()])
    return app


async def start_polling() -> None:
    logger.info('Starting polling')
    dp, bot = await setup_app()
    await bot.delete_webhook()
    logging.error('Dependencies launched')
    await dp.start_polling(bot)


if __name__ == '__main__':
    if settings.BOT_FASTAPI_HOST:
        uvicorn.run(
            'src.app:create_app',
            factory=True,
            host='127.0.0.1',
            port=settings.BOT_FASTAPI_PORT,
            workers=1,
        )
    else:
        asyncio.run(start_polling())
