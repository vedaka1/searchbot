from aiogram.fsm.state import State, StatesGroup


class UpdateFile(StatesGroup):
    category = State()
    file = State()


class Search(StatesGroup):
    category = State()
    search = State()
