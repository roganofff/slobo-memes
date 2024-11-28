from typing import Any, Awaitable, Callable, Dict

from aiogram import BaseMiddleware
from aiogram.types import TelegramObject, Message, CallbackQuery
from aiogram.dispatcher.flags import get_flag, extract_flags
from aiogram.utils.chat_action import ChatActionSender


class ChatActionMiddleware(BaseMiddleware):
    async def __call__(
        self,
        handler: Callable[[TelegramObject, Dict[str, Any]], Awaitable[Any]],
        event: TelegramObject,
        event_data: Dict[str, Any]
    ) -> Any:
        long_operation_type = get_flag(event_data, 'long_operation')
        if not long_operation_type:
            return await handler(event, event_data)
        if isinstance(event, CallbackQuery):
            chat_id = event.message.chat.id
        elif isinstance(event, Message):
            chat_id = event.chat.id
        else:
            return await handler(event, event_data)
        async with ChatActionSender(
            bot=event_data['bot'],
            action=long_operation_type, 
            chat_id=chat_id
        ):
            return await handler(event, event_data)
