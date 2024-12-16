import msgpack
from aio_pika import IncomingMessage

from src.schema.meme import RandomMeme
from src.services.meme import MemeService
from src.storage.rabbitmq import publish_message
from src.logger import logger, correlation_id_ctx


async def random_meme(message: IncomingMessage) -> None:
    async with message.process():
        correlation_id_ctx.set(message.correlation_id)
        message_body: RandomMeme = msgpack.unpackb(message.body)
        logger.info('Random meme message: %s', message_body)
        meme = await MemeService.get_random_meme(**message_body)
        await publish_message(
            message.reply_to,
            meme,
            correlation_id=message.correlation_id,
        )
