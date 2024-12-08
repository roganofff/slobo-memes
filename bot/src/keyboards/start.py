from aiogram.types import KeyboardButton, ReplyKeyboardMarkup

markup_keyboard = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(
                text='Главное меню',
            ),
        ],
    ],
    resize_keyboard=True,
)


async def keyboard() -> ReplyKeyboardMarkup:
    return markup_keyboard
