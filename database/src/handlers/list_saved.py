import msgpack
from aio_pika import IncomingMessage

from src.schema.meme import FirstSavedMeme, SavedMeme
from src.services.meme import MemeService
from src.storage.rabbitmq import publish_message
from src.logger import logger, correlation_id_ctx


async def first_meme(message: IncomingMessage) -> None:
    async with message.process():
        correlation_id_ctx.set(message.correlation_id)
        message_body: FirstSavedMeme = msgpack.unpackb(message.body)
        logger.info('First meme message: %s', message_body)
        meme = await MemeService.get_first_saved_meme(**message_body)
        await publish_message(
            message.reply_to,
            meme,
            correlation_id=message.correlation_id,
        )


async def get_meme(message: IncomingMessage) -> None:
    async with message.process():
        correlation_id_ctx.set(message.correlation_id)
        message_body: SavedMeme = msgpack.unpackb(message.body)
        logger.info('Get meme message: %s', message_body)
        meme = await MemeService.get_saved_meme_by_id(**message_body)
        await publish_message(
            message.reply_to,
            meme,
            correlation_id=message.correlation_id,
        )
