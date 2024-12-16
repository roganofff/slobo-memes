import msgpack
from aio_pika import IncomingMessage

from src.schema.meme import ChangeVisibility
from src.services.meme import MemeService
from src.storage.rabbitmq import publish_message
from src.logger import logger, correlation_id_ctx


async def change_visibility(message: IncomingMessage) -> None:
    async with message.process():
        correlation_id_ctx.set(message.correlation_id)
        message_body: ChangeVisibility = msgpack.unpackb(message.body)
        logger.info('Change meme visibility message: %s', message_body)
        meme = await MemeService.change_visibility(**message_body)
        await publish_message(
            message.reply_to,
            meme,
            correlation_id=message.correlation_id,
        )
