from datetime import datetime

import pytest
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery, Chat, Message, User

from src.handlers.list_saved import get_saved
from tests.mocking.rabbit import MockChannelPool, MockExchange


@pytest.mark.asyncio()
@pytest.mark.usefixtures('mock_publish_and_send_methods')
async def test_list_saved(
    mocker,
    mock_exchange: MockExchange,
    mock_channel_pool: MockChannelPool,
) -> None:
    query = CallbackQuery(
        id='test_query',
        from_user=User(id=123, is_bot=False, first_name='Test'),
        message=Message(
            message_id=1,
            date=datetime.now(),
            chat=Chat(id=456, type='private'),
            text='Test message',
        ),
        chat_instance='test_chat_instance',
        data='list_saved',
    )
    state = mocker.AsyncMock(spec=FSMContext)

    await get_saved(query=query, state=state)

    async with mock_channel_pool.acquire():
        mock_exchange.assert_has_calls([
            'first_saved',
            {'user_id': 123},
        ])
