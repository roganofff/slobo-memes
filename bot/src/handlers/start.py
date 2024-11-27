from aiogram.filters import CommandObject, CommandStart
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import default_state
from aiogram.types import Message

from src.handlers.router import router
from src.templates.env import render
from src.handlers.main_menu import main_menu


@router.message(CommandStart())
async def start(message: Message, state: FSMContext) -> None:
    await state.set_state(default_state)
    await message.answer(
        text=render('start.jinja2'),
    )
    await main_menu(message, state)
