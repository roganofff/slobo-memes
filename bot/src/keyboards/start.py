from aiogram.types import ReplyKeyboardMarkup
from aiogram.utils.keyboard import ReplyKeyboardBuilder


async def keyboard(resize_keyboard: bool = False) -> ReplyKeyboardMarkup:
    builder = ReplyKeyboardBuilder()
    builder.button(
        text='Главное меню',
    )
    builder.adjust(1)
    return builder.as_markup(resize_keyboard=resize_keyboard)