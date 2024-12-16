import msgpack
from aio_pika import IncomingMessage

from src.schema.meme import AddMeme
from src.services.meme import MemeService
from src.storage.rabbitmq import publish_message
from src.utils.image import Image
from src.logger import logger, correlation_id_ctx


async def add_meme(message: IncomingMessage) -> None:
    async with message.process():
        correlation_id_ctx.set(message.correlation_id)
        message_body: AddMeme = msgpack.unpackb(message.body)
        logger.info('Add meme message: %s', message_body)
        message_body['image_url'] = await Image.get_public_url(message_body['image_url'])
        meme = await MemeService.add_meme(**message_body)
        await publish_message(
            message.reply_to,
            meme,
            correlation_id=message.correlation_id,
        )
