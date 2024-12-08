from aiogram import F
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery

from src.handlers.main_menu import main_menu
from src.handlers.router import router
from src.states.states import MainStates, MemeStates
from src.storage.rabbitmq import publish_message_with_response


@router.callback_query(
    MemeStates.show,
    F.data == 'delete',
    flags={
        'new_state': MainStates.main_menu,
    },
)
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
