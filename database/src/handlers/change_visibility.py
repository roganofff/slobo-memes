import msgpack
from aio_pika import IncomingMessage

from src.services.meme import MemeService
from src.schema.meme import ChangeVisibility
from src.storage.rabbitmq import publish_message


async def change_visibility(message: IncomingMessage) -> None:
    async with message.process():
        message_body: ChangeVisibility = msgpack.unpackb(message.body)
        meme = await MemeService.change_visibility(**message_body)
        await publish_message(
            message.reply_to,
            meme,
            correlation_id=message.correlation_id,
        )
