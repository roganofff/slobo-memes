from aiogram.types import User, Chat, CallbackQuery
from aiogram.fsm.context import FSMContext
from unittest.mock import AsyncMock


class MockTgMessage(AsyncMock):
    def __init__(self, from_user: User, message_id: int, chat_id: int, **kwargs):
        super().__init__(**kwargs)
        self.from_user = from_user
        self.message_id = message_id
        self.chat = Chat(id=chat_id, type='private')
        self.text = 'Test message'


class MockCallbackQuery(CallbackQuery):
    def __init__(self, from_user: User, message: MockTgMessage, **kwargs):
        super().__init__(**kwargs)
        self.from_user = from_user
        self.message = message
        self.id = "mock_query_id"

    async def answer(self, text: str = "", show_alert: bool = False, cache_time: int = 0):
        print(f"Answer called with text: {text}, show_alert: {show_alert}, cache_time: {cache_time}")


class MockState(AsyncMock(spec=FSMContext)):
    ...