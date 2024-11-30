import msgpack
from aio_pika import IncomingMessage

from src.services.meme import MemeService
from src.schema.meme import RandomMeme
from src.storage.rabbitmq import publish_message


async def random_meme(message: IncomingMessage) -> None:
    async with message.process():
        message_body: RandomMeme = msgpack.unpackb(message.body)
        meme = await MemeService.get_random_meme(**message_body)
        await publish_message(
            message.reply_to,
            meme,
            correlation_id=message.correlation_id,
        )
