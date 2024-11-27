from aiogram import F
from aiogram.types import CallbackQuery, Message, LinkPreviewOptions
from aiogram.fsm.context import FSMContext

from src.handlers.router import router
from src.states.states import MainStates
from src.templates.env import render
from src.keyboards.main_menu import keyboard
from config.settings import settings
from src.utils.upload_image import upload_image


async def main_menu(message: Message, state: FSMContext) -> None:
    await message.delete()
    await state.set_state(MainStates.main_menu)
    user_profile_photo = await message.from_user.get_profile_photos()
    user_photo_id = user_profile_photo.photos[0][2].file_id
    bot_files_url = f'https://api.telegram.org/file/bot{settings.BOT_TOKEN}/'
    file_path = (await message.bot.get_file(user_photo_id)).file_path
    message = await message.answer(
        text=render(
            template_name='main_menu.jinja2',
            image_url=await upload_image(f'{bot_files_url}{file_path}'),
            user_username=message.from_user.username,
            user_id=message.from_user.id,
        ),
        reply_markup=await keyboard(),
        link_preview_options=LinkPreviewOptions(
            show_above_text=True,
        )
    )