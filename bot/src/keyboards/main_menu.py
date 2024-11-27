from aiogram.types import InlineKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder


async def keyboard() -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()
    builder.button(
        text='Добавить мем',
        callback_data='add_meme',
    )
    builder.adjust(1)
    return builder.as_markup()