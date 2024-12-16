import msgpack
from aio_pika import IncomingMessage

from src.schema.meme import MemeSaves
from src.services.meme import MemeService
from src.storage.rabbitmq import publish_message
from src.logger import logger, correlation_id_ctx


async def add_to_saved(message: IncomingMessage) -> None:
    async with message.process():
        correlation_id_ctx.set(message.correlation_id)
        message_body: MemeSaves = msgpack.unpackb(message.body)
        logger.info('Add meme to saved message: %s', message_body)
        meme = await MemeService.add_to_saved(**message_body)
        await publish_message(
            message.reply_to,
            meme,
            correlation_id=message.correlation_id,
        )


async def remove_from_saved(message: IncomingMessage) -> None:
    async with message.process():
        correlation_id_ctx.set(message.correlation_id)
        message_body: MemeSaves = msgpack.unpackb(message.body)
        logger.info('Remove meme from saved message: %s', message_body)
        meme = await MemeService.remove_from_saved(**message_body)
        await publish_message(
            message.reply_to,
            meme,
            correlation_id=message.correlation_id,
        )
