import msgpack
from aio_pika import IncomingMessage

from src.services.meme import MemeService
from src.schema.meme import RateMeme, RemoveRating
from src.storage.rabbitmq import publish_message


async def rate_meme(message: IncomingMessage) -> None:
    async with message.process():
        message_body: RateMeme = msgpack.unpackb(message.body)
        meme = await MemeService.rate_meme(**message_body)
        await publish_message(
            message.reply_to,
            meme,
            correlation_id=message.correlation_id,
        )


async def remove_rating(message: IncomingMessage) -> None:
    async with message.process():
        message_body: RemoveRating = msgpack.unpackb(message.body)
        meme = await MemeService.remove_rating(**message_body)
        await publish_message(
            message.reply_to,
            meme,
            correlation_id=message.correlation_id,
        )