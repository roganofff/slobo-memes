from aiogram import F
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery, LinkPreviewOptions

from src.handlers.router import router
from src.keyboards.meme import keyboard
from src.states.states import MainStates, MemeStates
from src.storage.rabbitmq import publish_message_with_response
from src.templates.env import render
from src.utils.edit_or_send_message import edit_or_send_message

default_flags = {
    'new_state': MemeStates.show,
}


async def random_meme(query: CallbackQuery, state: FSMContext, public_only: bool) -> None:
    publish_result = await publish_message_with_response(
        routing_key='random_meme',
        message={
            'user_id': query.from_user.id,
            'public_only': public_only,
        },
    )
    if not publish_result:
        query.answer('Мемов нет :(')
        return
    query.answer()
    message_args = {
        'text': render(
            'meme.jinja2',
            description=publish_result['description'],
        ),
        'reply_markup': await keyboard(
            is_owner=publish_result['creator_id'] == query.from_user.id,
            is_saved=publish_result['is_saved'],
            is_public=publish_result['is_public'],
            likes=publish_result['likes'],
            dislikes=publish_result['dislikes'],
            user_rating=publish_result['user_rating'],
            random_type='public' if public_only else 'saved',
        ),
        'chat_id': query.message.chat.id,
        'link_preview_options': LinkPreviewOptions(
            url=publish_result['image_url'],
            show_above_text=True,
            prefer_large_media=True,
        ),
    }
    await edit_or_send_message(message_args, query.message.message_id)
    await state.set_data(
        {
            'meme_id': publish_result['id'],
            'public_only': public_only,
        },
    )


@router.callback_query(MainStates.main_menu, F.data == 'random_public', flags=default_flags)
@router.callback_query(MemeStates.show, F.data == 'random_public')
async def random_public_meme(query: CallbackQuery, state: FSMContext) -> None:
    await random_meme(query, state, public_only=True)


@router.callback_query(MainStates.main_menu, F.data == 'random_saved', flags=default_flags)
@router.callback_query(MemeStates.show, F.data == 'random_saved')
async def random_public_meme(query: CallbackQuery, state: FSMContext) -> None:
    await random_meme(query, state, public_only=False)
