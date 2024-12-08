import msgpack
from aio_pika import IncomingMessage

from src.schema.meme import FirstSavedMeme, SavedMeme
from src.services.meme import MemeService
from src.storage.rabbitmq import publish_message


async def first_meme(message: IncomingMessage) -> None:
    async with message.process():
        message_body: FirstSavedMeme = msgpack.unpackb(message.body)
        meme = await MemeService.get_first_saved_meme(**message_body)
        await publish_message(
            message.reply_to,
            meme,
            correlation_id=message.correlation_id,
        )


async def get_meme(message: IncomingMessage) -> None:
    async with message.process():
        message_body: SavedMeme = msgpack.unpackb(message.body)
        meme = await MemeService.get_saved_meme_by_id(**message_body)
        await publish_message(
            message.reply_to,
            meme,
            correlation_id=message.correlation_id,
        )
