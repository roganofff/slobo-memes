import uuid

import aio_pika
import msgpack
import pytest
from pathlib import Path

from sqlalchemy import select, func

from config.settings import settings
from bot.src.app import setup_app
from database.src.models.models import Meme
from database.src.schema.meme import AddMeme
from tests.mocking.rabbit import MockExchange

BASE_DIR = Path(__file__).parent
SEED_DIR = BASE_DIR / 'seeds'


@pytest.mark.parametrize(
    ('predefined_queue', 'seeds', 'correlation_id'),
    [
        (
            AddMeme(creator_id=1, description='ccc', image_url='ccc'),
            [SEED_DIR / 'public.meme.json'],
            str(uuid.uuid4()),
        ),
    ]
)
@pytest.mark.asyncio()
@pytest.mark.usefixtures('_load_queue', '_load_seeds')
async def test_handle_gift(db_session, predefined_queue, correlation_id, mock_exchange: MockExchange) -> None:
    await setup_app()
    expected_routing_key = settings.USER_MEME_QUEUE_TEMPLATE.format(user_id=predefined_queue['user_id'])

    expected_calls = []
    async with db_session:
        not_fetched = await db_session.execute(select(Meme).order_by(func.random()))
        tuple_rows = not_fetched.all()
        memes = [row for row, in tuple_rows]

        for meme in memes:
            expected_message = aio_pika.Message(
                msgpack.packb({
                    'description': meme.description,
                    'image_url': meme.image_url,
                    'is_public': meme.is_public,
                    'ratings': meme.ratings,
                    'saved_by': meme.saved_by
                }),
                correlation_id=correlation_id,
            )

            expected_calls.append(
                ('publish', (expected_message,), {'routing_key': expected_routing_key})
            )

        mock_exchange.assert_has_calls(expected_calls, any_order=True)