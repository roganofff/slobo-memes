from aiogram import F
from aiogram.types import CallbackQuery, Message
from aiogram.fsm.context import FSMContext

from src.handlers.router import router
from src.states.states import MainStates
from src.templates.env import render
from src.keyboards.main_menu import keyboard
from config.settings import settings


async def main_menu(message: Message, state: FSMContext) -> None:
    await message.delete()
    await state.set_state(MainStates.main_menu)
    message = await message.answer(
        text=render(
            template_name='main_menu.jinja2',
            user_username=message.from_user.username,
            user_id=message.from_user.id,
        ),
        reply_markup=await keyboard(),
    )