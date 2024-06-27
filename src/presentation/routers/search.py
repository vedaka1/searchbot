from logging import getLogger

from aiogram import Bot, F, Router, filters, types
from aiogram.fsm.context import FSMContext
from dishka import AsyncContainer

from application.common.states import Search
from application.usecases.callbacks.request_access import RequestAccessCallback
from application.usecases.commands.request_access import RequestAccessCommand
from application.usecases.document.get_document import GetDocument
from application.usecases.employe.get_employe import GetEmploye
from application.usecases.users.create_user import CreateUser
from presentation.common.keyboards import search_category_keyboard
from presentation.texts.text import text

logger = getLogger()
search_router = Router()


@search_router.message(filters.Command("request_access"))
async def cmd_request_access(
    message: types.Message, bot: Bot, state: FSMContext, container: AsyncContainer
):
    async with container() as di_container:
        request_access_command_interactor = await di_container.get(RequestAccessCommand)
        await request_access_command_interactor(message=message, bot=bot, state=state)


@search_router.callback_query(F.data.startswith("requestAccess_"))
async def callback_request_access(
    callback: types.CallbackQuery,
    bot: Bot,
    container: AsyncContainer,
):
    async with container() as di_container:
        request_access_callback_interactor = await di_container.get(
            RequestAccessCallback
        )
        await request_access_callback_interactor(callback=callback, bot=bot)


@search_router.message(filters.Command("start"))
async def cmd_start(message: types.Message, container: AsyncContainer):
    async with container() as di_container:
        create_user = await di_container.get(CreateUser)
        await create_user(message.from_user.id, message.from_user.username)
        await message.answer(text["start"])


@search_router.message(Search.search)
async def search_error(message: types.Message) -> None:
    await message.reply("Подождите, идет поиск...")


@search_router.message(filters.Command("search"))
async def cmd_search(message: types.Message, state: FSMContext):
    await state.clear()
    await state.set_state(Search.category)
    await message.answer(
        "Выберите категорию поиска:",
        reply_markup=types.InlineKeyboardMarkup(
            inline_keyboard=search_category_keyboard
        ),
    )


@search_router.callback_query(Search.category, F.data.startswith("search_"))
async def callback_search(
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
async def search(message: types.Message, container: AsyncContainer, state: FSMContext):
    await state.set_state(Search.search)
    data = await state.get_data()
    category = data.get("category")
    async with container() as di_container:
        if category == "Сотрудник":
            get_employe_interactor = await di_container.get(GetEmploye)
            await get_employe_interactor(message=message)
        if category == "Документ":
            get_document_interactor = await di_container.get(GetDocument)
            await get_document_interactor(message=message)

        await state.clear()
