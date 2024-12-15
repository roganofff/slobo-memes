import msgpack
from aio_pika import IncomingMessage

from src.schema.meme import FirstSavedMeme
from src.services.meme import MemeService
from src.storage.rabbitmq import publish_message


async def popular_meme(message: IncomingMessage) -> None:
    async with message.process():
        message_body: FirstSavedMeme = msgpack.unpackb(message.body)
        meme = await MemeService.popular_meme(**message_body)
        await publish_message(
            message.reply_to,
            meme,
            correlation_id=message.correlation_id,
        )
