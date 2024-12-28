from aiogram import F
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery, LinkPreviewOptions

from src.handlers.router import router
from src.keyboards.meme import keyboard
from src.states.states import MainStates, MemeStates
from src.storage.rabbitmq import publish_message_with_response
from src.templates.env import render
from src.utils.edit_or_send_message import edit_or_send_message


async def get_saved(
    query: CallbackQuery,
    state: FSMContext,
    saved_id: str | None = None,
) -> None:
    message = {
        'user_id': query.from_user.id,
    }
    if saved_id:
        routing_key = 'get_saved'
        message['saved_id'] = str(saved_id)
    else:
        routing_key = 'first_saved'
    publish_result = await publish_message_with_response(
        routing_key=routing_key,
        message=message,
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
            pagination=publish_result['pagination'],
        ),
        'chat_id': query.message.chat.id,
        'link_preview_options': LinkPreviewOptions(
            url=publish_result['image_url'],
            show_above_text=True,
            prefer_large_media=True,
        ),
    }
    await state.set_state(MemeStates.show)
    await edit_or_send_message(message_args, query.message.message_id)
    await state.set_data(
        {
            'meme_id': publish_result['id'],
            'next_id': publish_result['pagination'][1],
            'prev_id': publish_result['pagination'][0],
        },
    )


@router.callback_query(
    MainStates.main_menu,
    F.data == 'list_saved',
    flags={
        'new_state': MemeStates.show,
    },
)
async def first_saved(query: CallbackQuery, state: FSMContext) -> None:
    await get_saved(query, state)


@router.callback_query(
    MemeStates.show,
    F.data == 'next_meme',
    flags={
        'new_state': MemeStates.next,
    },
)
async def next_saved(query: CallbackQuery, state: FSMContext) -> None:
    data = await state.get_data()
    await state.set_state(MemeStates.show)
    await get_saved(
        query,
        state,
        data.get('next_id'),
    )


@router.callback_query(
    MemeStates.show,
    F.data == 'previous_meme',
    flags={
        'new_state': MemeStates.prev,
    },
)
async def prev_saved(query: CallbackQuery, state: FSMContext) -> None:
    data = await state.get_data()
    await state.set_state(MemeStates.show)
    await get_saved(
        query,
        state,
        data.get('prev_id'),
    )
