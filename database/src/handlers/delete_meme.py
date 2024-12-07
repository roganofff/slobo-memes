import msgpack
from aio_pika import IncomingMessage

from src.services.meme import MemeService
from src.schema.meme import MemeSaves
from src.storage.rabbitmq import publish_message


async def delete_meme(message: IncomingMessage) -> None:
    async with message.process():
        message_body: MemeSaves = msgpack.unpackb(message.body)
        meme = await MemeService.delete_meme(**message_body)
        await publish_message(
            message.reply_to,
            meme,
            correlation_id=message.correlation_id,
        )
