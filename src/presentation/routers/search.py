from aiogram import F, Router, filters, types
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from dishka import AsyncContainer

from application.usecases.document.get_document import GetDocument
from application.usecases.employe.get_employe import GetEmploye
from presentation.common.keyboards import category_keyboard
from presentation.texts.text import text

search_router = Router()


class Search(StatesGroup):
    category = State()
    search = State()


@search_router.message(Search.search)
async def generate_error(message: types.Message) -> None:
    await message.reply("Подождите, идет поиск...")


@search_router.message(filters.Command("start"))
async def start(message: types.Message):
    await message.answer(text["start"])


@search_router.message(filters.Command("search"))
async def search(message: types.Message, state: FSMContext)
    await state.clear()
    await state.set_state(Search.category)
    await message.answer(
        "Выберите категорию поиска:",
        reply_markup=types.InlineKeyboardMarkup(inline_keyboard=category_keyboard),
    )


@search_router.callback_query(Search.category, F.data.startswith("search_"))
async def select_subscription_callback(
    callback: types.CallbackQuery,
    state: FSMContext,
):
    user_choice = callback.data.split("_")[1]
    await state.update_data(category=user_choice)
    if user_choice == "Сотрудник":
        await callback.message.edit_text("Введите ФИО или должность сотрудника")
    if user_choice == "Документ":
        await callback.message.edit_text("Введите название или реквизиты документа")


@search_router.message(Search.category)
async def get_employe(
    message: types.Message, container: AsyncContainer, state: FSMContext
):
    await state.set_state(Search.search)
    data = await state.get_data()
    category = data.get("category")
    if category == "Сотрудник":
        async with container() as di_container:
            get_employe = await di_container.get(GetEmploye)
            result = await get_employe(message.text)
            await state.clear()
            await message.answer(result, parse_mode="MarkDownV2")
    if category == "Документ":
        async with container() as di_container:
            get_employe = await di_container.get(GetDocument)
            result = await get_employe(message.text)
            await state.clear()
            await message.answer(result, parse_mode="MarkDownV2")
