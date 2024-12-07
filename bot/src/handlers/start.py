from aiogram.filters import CommandObject, CommandStart
from aiogram.fsm.context import FSMContext
from aiogram.types import Message

from src.handlers.router import router
from src.templates.env import render
from src.handlers.main_menu import main_menu_message
from src.keyboards.start import keyboard
from src.states.states import MainStates


@router.message(CommandStart())
async def start(message: Message, state: FSMContext) -> None:
    await message.answer(
        text=render('start.jinja2'),
        reply_markup=await keyboard()
    )
    await main_menu_message(message, state)
    await state.set_state(MainStates.main_menu)
