from aiogram import F
from aiogram.types import CallbackQuery, Message, LinkPreviewOptions
from aiogram.fsm.context import FSMContext
from types import MappingProxyType

from src.handlers.router import router
from src.states import states
from src.templates.env import render
from src.keyboards.main_menu import keyboard
from config.settings import settings
from src.utils.image import Image


default_flags = {
    'long_operation': 'typing',
    'new_state': states.MainStates.main_menu
}


async def main_menu(message: Message, query: CallbackQuery | None = None) -> None:
    event = query if query else message
    user_profile_photo = await event.from_user.get_profile_photos()
    user_photo_id = user_profile_photo.photos[0][-1].file_id
    file_url = await Image.get_telegram_url(user_photo_id)
    message_args = {
        'text': render(
            template_name='main_menu.jinja2',
            user_username=event.from_user.username,
            user_id=event.from_user.id,
        ),
        'reply_markup': await keyboard(),
        'link_preview_options': LinkPreviewOptions(
            url=await Image.get_public_url(file_url),
            show_above_text=True,
        ),
    }
    if query:
        await message.edit_text(**message_args)
        return
    await message.answer(**message_args)


@router.message(
    F.text == 'Главное меню',
    flags={
        'long_operation': 'typing',
        'new_state': states.MainStates.main_menu
    },
)
async def main_menu_message(message: Message, state: FSMContext) -> None:
    await message.delete()
    await main_menu(message)


@router.callback_query(
    states.AddMemeStates.request_meme,
    F.data == 'main_menu',
    flags=default_flags,
)
async def main_menu_callback(query: CallbackQuery, state: FSMContext) -> None:
    await query.answer()
    await main_menu(query.message, query)
