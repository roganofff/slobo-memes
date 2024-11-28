from aiogram.fsm.state import StatesGroup, State


class MainStates(StatesGroup):
    main_menu = State()


class AddMemeStates(StatesGroup):
    request_meme = State()
    process_meme = State()


class MemeStates(StatesGroup):
    show = State()
