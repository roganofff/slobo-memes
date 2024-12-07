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
from src.handlers.main_menu import main_menu


@router.callback_query(MemeStates.show, F.data == 'make_public')
async def delete_meme(query: CallbackQuery, state: FSMContext) -> None:
    data = await state.get_data()
    meme_id = data['meme_id']
    publish_result = await publish_message_with_response(
        routing_key='delete_meme',
        message={
            'user_id': query.from_user.id,
            'meme_id': meme_id,
        },
    )
    if not publish_result:
        query.answer('Ошибка :o')
        return
    query.answer('Успешно!')
    await main_menu(query.message, query)
