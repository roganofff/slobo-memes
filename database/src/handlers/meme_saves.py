import msgpack
from aio_pika import IncomingMessage

from src.services.meme import MemeService
from src.schema.meme import MemeSaves
from src.storage.rabbitmq import publish_message


async def add_to_saved(message: IncomingMessage) -> None:
    async with message.process():
        message_body: MemeSaves = msgpack.unpackb(message.body)
        meme = await MemeService.add_to_saved(**message_body)
        await publish_message(
            message.reply_to,
            meme,
            correlation_id=message.correlation_id,
        )


async def remove_from_saved(message: IncomingMessage) -> None:
    async with message.process():
        message_body: MemeSaves = msgpack.unpackb(message.body)
        meme = await MemeService.remove_from_saved(**message_body)
        await publish_message(
            message.reply_to,
            meme,
            correlation_id=message.correlation_id,
        )