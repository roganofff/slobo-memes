from typing import Optional

from aiogram.types import InlineKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder


async def keyboard(
    is_owner: bool,
    is_saved: bool,
    is_public: bool,
    likes: int,
    dislikes: int,
    user_rating: Optional[bool] = None,
    random_type: Optional[str] = None,
    pagination: tuple[str, str] = None,
) -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()
    builder.button(
        text='Назад',
        callback_data='main_menu'
    )
    if is_saved:
        personal_text = 'Удалить из СВОих'
        personal_data = 'remove_from_saved'
    else:
        personal_text = 'Добавить к себе'
        personal_data = 'add_to_saved'
    builder.button(
            text=personal_text,
            callback_data=personal_data,
        )
    if is_public:
        if user_rating:
            like_text = f'[Нрав {likes}]'
            like_data = 'remove_rating'
        else:
            like_text = f'Нрав {likes}'
            like_data = 'like'
        builder.button(
            text=like_text,
            callback_data=like_data,
        )
        if not user_rating:
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
    if pagination:
        if pagination[0]:
            builder.button(
                text='Пред',
                callback_data='previous_meme',
            )
        if pagination[1]:
            builder.button(
                text='След',
                callback_data='next_meme',
            )
    if is_public:
        if is_owner:
            builder.adjust(1, 1, 2, 1, 1, 2)
        else:
            builder.adjust(1, 1, 2, 2)
    else:
        if is_owner:
            builder.adjust(1, 1, 1, 1, 2)
        else:
            builder.adjust(1, 1, 2)
    return builder.as_markup()
