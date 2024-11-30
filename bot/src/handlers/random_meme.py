from aiogram import F
from aiogram.types import CallbackQuery, LinkPreviewOptions
from aiogram.fsm.context import FSMContext

from src.handlers.router import router
from src.storage.rabbitmq import publish_message_with_response
from src.utils.edit_or_send_message import edit_or_send_message
from src.templates.env import render
from src.keyboards.meme import keyboard
from src.states.states import MemeStates, MainStates


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
    await state.set_state(MemeStates.show)
    await edit_or_send_message(message_args, query.message.message_id)
    await state.set_data(
        {
            'meme_id': publish_result['id'],
            'public_only': public_only,
        }
    )


@router.callback_query(MainStates.main_menu, F.data == 'random_public')
@router.callback_query(MemeStates.show, F.data == 'random_public')
async def random_public_meme(query: CallbackQuery, state: FSMContext) -> None:
    await random_meme(query, state, public_only=True)


@router.callback_query(MainStates.main_menu, F.data == 'random_saved')
@router.callback_query(MemeStates.show, F.data == 'random_saved')
async def random_public_meme(query: CallbackQuery, state: FSMContext) -> None:
    await random_meme(query, state, public_only=True)
