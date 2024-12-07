from typing import Any, Awaitable, Callable, Dict

from aiogram import BaseMiddleware
from aiogram.types import TelegramObject, Message, CallbackQuery
from aiogram.fsm.context import FSMContext
from aiogram.dispatcher.flags import get_flag, extract_flags


class StateMiddleware(BaseMiddleware):
    async def __call__(
        self,
        handler: Callable[[TelegramObject, Dict[str, Any]], Awaitable[Any]],
        event: TelegramObject,
        event_data: Dict[str, Any]
    ) -> Any:
        state: FSMContext = event_data['state']
        new_state = get_flag(event_data, 'new_state')
        if not new_state:
            return await handler(event, event_data)
        if await state.get_state() != new_state:
            await state.set_state(new_state)
            event_data['state'] = state
            return await handler(event, event_data)
        if isinstance(event, CallbackQuery):
            await event.answer()
        if isinstance(event, Message):
            await event.delete()
