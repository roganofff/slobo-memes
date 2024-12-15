import uuid
import pytest

from aiogram.types import User, CallbackQuery

from src.handlers.list_saved import first_meme
from tests.mocking.rabbit import MockMessage

@pytest.mark.parametrize(
    ('predefined_queue', 'predefined_keyboard_args'),
    [
        (
            {'creator_id': 1, 'description': 'ae', 'image_url': 'cac'},
            {
                'is_owner': True,
                'is_saved': False,
                'is_public': True,
                'likes': 0,
                'dislikes': 0,
            },
        ),
        (
            None,
            {
                'is_owner': True,
                'is_saved': False,
                'is_public': True,
                'likes': 0,
                'dislikes': 0,
            },
        ),
    ]
)
@pytest.mark.asyncio()
async def test_list_saved(predefined_queue, predefined_keyboard_args) -> None:
    user = User(id=1, is_bot=False, is_premium=False, last_name='test', first_name='test')
    message = MockMessage(body=b'aaa', correlation_id=str(uuid.uuid4()))

    await first_meme(message=message)

    if predefined_queue:
        image_url = predefined_queue['image_url']
        message.assert_has_calls([
            'list_saved',
            {
                'image_url': predefined_queue['image_url'],
            }
        ])
    else:
        message.assert_has_calls([
            ('list_saved', ('Мемов нет :(', ))
        ])
