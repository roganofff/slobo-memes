from typing import Union

from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

from src.utils.mark import Mark
from src.utils.random_type import RandomType

async def keyboard(
    is_owner: bool,
    is_saved: bool,
    is_public: bool,
    likes: int,
    dislikes: int,
    user_rating: Union[Mark, None] = None,
    random_type: Union[RandomType, None] = None,
) -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()
    builder.button(
        text='Назад',
        callback_data='main_menu'
    )
    if is_saved:
        personal_text = 'Удалить из СВОих'
        personal_data = 'delete_saved'
    else:
        personal_text = 'Добавить к себе'
        personal_data = 'add_saved'
    builder.button(
            text=personal_text,
            callback_data=personal_data,
        )
    if is_public:
        if user_rating == True:
            like_text = f'[Нрав {likes}]'
            like_data = 'remove_rating'
        else:
            like_text = f'Нрав {likes}'
            like_data = 'like'
        builder.button(
            text=like_text,
            callback_data=like_data,
        )
        if user_rating == False:
            dislike_text = f'[Ненрав {dislikes}]'
            dislike_data = 'remove_rating'
        else:
            dislike_text = f'Ненрав {dislikes}'
            dislike_data = 'dislike'
        builder.button(
            text=dislike_text,
            callback_data=dislike_data,
        )
        if is_owner:
            builder.button(
                text='Сделать приватным',
                callback_data='make_private',
            )
    elif is_owner:
        builder.button(
            text='Сделать публичным',
            callback_data='make_public',
        )
    if is_owner:
        builder.button(
            text='Удалить',
            callback_data='delete',
        )
    if random_type:
        builder.button(
            text='Еще!',
            callback_data=f'random_{random_type}',
        )
    if is_public:
        builder.adjust(1, 1, 2, 1, 1, 1)
    else:
        builder.adjust(1, repeat=True)
    return builder.as_markup()
