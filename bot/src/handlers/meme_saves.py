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


async def meme_saves(query: CallbackQuery, state: FSMContext, save: bool) -> None:
    data = await state.get_data()
    public_only = data['public_only']
    meme_id = data['meme_id']
    routing_key = 'add_to_saved' if save else 'remove_from_saved'
    publish_result = await publish_message_with_response(
        routing_key=routing_key,
        message={
            'user_id': query.from_user.id,
            'meme_id': meme_id,
        },
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


@router.callback_query(MemeStates.show, F.data == 'add_to_saved')
async def add_to_saved(query: CallbackQuery, state: FSMContext) -> None:
    await meme_saves(query, state, save=True)


@router.callback_query(MemeStates.show, F.data == 'remove_from_saved')
async def remove_from_saved(query: CallbackQuery, state: FSMContext) -> None:
    await meme_saves(query, state, save=False)
