import msgpack
from aio_pika import IncomingMessage

from src.schema.meme import RateMeme, RemoveRating
from src.services.meme import MemeService
from src.storage.rabbitmq import publish_message
from src.logger import logger, correlation_id_ctx


async def rate_meme(message: IncomingMessage) -> None:
    async with message.process():
        correlation_id_ctx.set(message.correlation_id)
        message_body: RateMeme = msgpack.unpackb(message.body)
        logger.info('Rate meme message: %s', message_body)
        meme = await MemeService.rate_meme(**message_body)
        await publish_message(
            message.reply_to,
            meme,
            correlation_id=message.correlation_id,
        )


async def remove_rating(message: IncomingMessage) -> None:
    async with message.process():
        correlation_id_ctx.set(message.correlation_id)
        message_body: RemoveRating = msgpack.unpackb(message.body)
        logger.info('Remove meme message: %s', message_body)
        meme = await MemeService.remove_rating(**message_body)
        await publish_message(
            message.reply_to,
            meme,
            correlation_id=message.correlation_id,
        )
