import msgpack
from aio_pika import IncomingMessage

from src.services.meme import MemeService
from src.schema.meme import AddMeme
from src.utils.image import Image
from src.storage.rabbitmq import publish_message


async def add_meme(message: IncomingMessage) -> None:
    async with message.process():
        message_body: AddMeme = msgpack.unpackb(message.body)
        message_body['image_url'] = await Image.get_public_url(message_body['image_url'])
        meme = await MemeService.add_meme(**message_body)
        await publish_message(
            message.reply_to,
            meme,
            correlation_id=message.correlation_id,
        )
