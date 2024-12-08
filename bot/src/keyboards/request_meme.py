from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

markup_keyboard = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(
                text='Назад',
                callback_data='main_menu',
            ),
        ],
    ],
)


async def keyboard() -> InlineKeyboardMarkup:
    return markup_keyboard
