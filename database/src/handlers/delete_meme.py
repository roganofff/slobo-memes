import msgpack
from aio_pika import IncomingMessage

from src.schema.meme import MemeSaves
from src.services.meme import MemeService
from src.storage.rabbitmq import publish_message
from src.logger import logger, correlation_id_ctx


async def delete_meme(message: IncomingMessage) -> None:
    async with message.process():
        correlation_id_ctx.set(message.correlation_id)
        message_body: MemeSaves = msgpack.unpackb(message.body)
        logger.info('Delete meme message: %s', message_body)
        meme = await MemeService.delete_meme(**message_body)
        await publish_message(
            message.reply_to,
            meme,
            correlation_id=message.correlation_id,
        )
