from aiogram import F
from aiogram.types import CallbackQuery, Message, LinkPreviewOptions
from aiogram.fsm.context import FSMContext

from src.handlers.router import router
from src.states.states import MainStates
from src.templates.env import render
from src.keyboards.main_menu import keyboard
from config.settings import settings
from src.utils.image import Image


async def main_menu(message: Message, state: FSMContext) -> None:
    await message.delete()
    await state.set_state(MainStates.main_menu)
    user_profile_photo = await message.from_user.get_profile_photos()
    user_photo_id = user_profile_photo.photos[0][-1].file_id
    file_url = await Image.get_telegram_url(user_photo_id)
    message = await message.answer(
        text=render(
            template_name='main_menu.jinja2',
            image_url=await Image.get_public_url(file_url),
            user_username=message.from_user.username,
            user_id=message.from_user.id,
        ),
        reply_markup=await keyboard(),
        link_preview_options=LinkPreviewOptions(
            show_above_text=True,
        )
    )