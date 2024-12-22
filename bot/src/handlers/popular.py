from aiogram import F
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery, LinkPreviewOptions

from src.metrics import SEND_MESSAGE, track_latency
from src.handlers.router import router
from src.keyboards.meme import keyboard
from src.states.states import MainStates, MemeStates
from src.storage.rabbitmq import publish_message_with_response
from src.templates.env import render
from src.utils.edit_or_send_message import edit_or_send_message


@router.callback_query(
    MainStates.main_menu,
    F.data == 'popular',
    flags={
        'new_state': MemeStates.show,
    },
)
@track_latency('popular_meme')
async def popular_meme(query: CallbackQuery, state: FSMContext) -> None:
    publish_result = await publish_message_with_response(
        routing_key='popular_meme',
        message={
            'user_id': query.from_user.id,
        },
    )
    if not publish_result:
        query.answer('Мема нет :(')
        return
    SEND_MESSAGE.inc()
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
        },
    )
