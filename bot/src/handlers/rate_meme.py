from typing import Optional

from aiogram import F
from aiogram.types import CallbackQuery, LinkPreviewOptions
from aiogram.fsm.context import FSMContext

from src.handlers.router import router
from src.storage.rabbitmq import publish_message_with_response
from src.utils.edit_or_send_message import edit_or_send_message
from src.templates.env import render
from src.keyboards.meme import keyboard
from src.states.states import MemeStates


async def rate_meme(query: CallbackQuery, state: FSMContext, rating: Optional[bool] = None) -> None:
    data = await state.get_data()
    public_only = data['public_only']
    meme_id = data['meme_id']
    message_args = {
        'user_id': query.from_user.id,
        'meme_id': meme_id,
    }
    if rating is not None:
        message_args['new_rating'] = rating
        publish_result = await publish_message_with_response(
            routing_key='rate_meme',
            message=message_args,
        )
    else:
        publish_result = await publish_message_with_response(
            routing_key='remove_rating',
            message=message_args,
        )
    if not publish_result:
        query.answer('Ошибка :o')
        return
    query.answer()
    message_args = {
        'text': render(
            'meme.jinja2',
            description=publish_result['description']
        ),
        'reply_markup': await keyboard(
            is_owner=publish_result['creator_id'] == query.from_user.id,
            is_saved=publish_result['is_saved'],
            is_public=publish_result['is_public'],
            likes=publish_result['likes'],
            dislikes=publish_result['dislikes'],
            user_rating=publish_result['user_rating'],
            random_type='public' if public_only else 'saved'
        ),
        'chat_id': query.message.chat.id,
        'link_preview_options': LinkPreviewOptions(
            url=publish_result['image_url'],
            show_above_text=True,
            prefer_small_media=True,
        ),
    }
    await edit_or_send_message(message_args, query.message.message_id)


@router.callback_query(MemeStates.show, F.data == 'like')
async def like_meme(query: CallbackQuery, state: FSMContext) -> None:
    await rate_meme(query, state, rating=True)


@router.callback_query(MemeStates.show, F.data == 'dislike')
async def dislike_meme(query: CallbackQuery, state: FSMContext) -> None:
    await rate_meme(query, state, rating=False)


@router.callback_query(MemeStates.show, F.data == 'remove_rating')
async def remove_rating(query: CallbackQuery, state: FSMContext) -> None:
    await rate_meme(query, state)
