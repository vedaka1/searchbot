from logging import getLogger

from aiogram import Bot, F, Router, filters, types
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from dishka import AsyncContainer

from application.usecases.document.get_document import GetDocument
from application.usecases.employe.get_employe import GetEmploye
from application.usecases.users.create_user import CreateUser
from application.usecases.users.get_user import GetHeadAdminId
from application.usecases.users.update_user import UpdateUserRole
from domain.common.response import Response
from presentation.common.keyboards import category_keyboard, request_access_keyboard
from presentation.texts.text import text

logger = getLogger()
search_router = Router()


class Search(StatesGroup):
    category = State()
    search = State()


@search_router.message(Search.search)
async def search_error(message: types.Message) -> None:
    await message.reply("Подождите, идет поиск...")


@search_router.message(filters.Command("start"))
async def cmd_start(message: types.Message, container: AsyncContainer):
    async with container() as di_container:
        create_user = await di_container.get(CreateUser)
        await create_user(message.from_user.id, message.from_user.username)
    await message.answer(text["start"])


@search_router.message(filters.Command("search"))
async def cmd_search(message: types.Message, state: FSMContext):
    await state.clear()
    await state.set_state(Search.category)
    await message.answer(
        "Выберите категорию поиска:",
        reply_markup=types.InlineKeyboardMarkup(inline_keyboard=category_keyboard),
    )


@search_router.callback_query(Search.category, F.data.startswith("search_"))
async def callback_select_subscription(
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
    async with container() as di_container:
        if category == "Сотрудник":
            get_employe = await di_container.get(GetEmploye)
            result = await get_employe(message.text)
            await state.clear()
            await message.answer(result, parse_mode="MarkDownV2")
        if category == "Документ":
            get_employe = await di_container.get(GetDocument)
            result = await get_employe(message.text)
            await state.clear()
            await message.answer(result, parse_mode="MarkDownV2")


@search_router.message(filters.Command("request_access"))
async def cmd_request_access(
    message: types.Message, bot: Bot, container: AsyncContainer
):
    async with container() as di_container:
        get_head_admin = await di_container.get(GetHeadAdminId)
        create_user = await di_container.get(CreateUser)
        await create_user(message.from_user.id, message.from_user.username)
        head_admin_id = await get_head_admin()

    text = Response(
        f"Пользователь запросил права администратора\n\n*ID:* {message.from_user.id}\n*username:* {message.from_user.username}"
    ).value
    await bot.send_message(
        chat_id=head_admin_id,
        text=text,
        reply_markup=types.InlineKeyboardMarkup(
            inline_keyboard=request_access_keyboard(message.from_user.id)
        ),
        parse_mode="MarkDownV2",
    )
    await message.answer("Запрос отправлен")


@search_router.callback_query(F.data.startswith("requestAccess_"))
async def callback_request_access(
    callback: types.CallbackQuery,
    bot: Bot,
    container: AsyncContainer,
):
    user_choice = callback.data.split("_")[1]
    from_user = callback.data.split("_")[2]
    if user_choice == "accept":
        async with container() as di_container:
            update_user_role = await di_container.get(UpdateUserRole)
            await update_user_role(user_id=int(from_user))
            await callback.message.delete()
            await bot.send_message(
                chat_id=from_user, text="Ваш запрос на права администратора был одобрен"
            )
    if user_choice == "reject":
        await callback.message.delete()
        await bot.send_message(
            chat_id=from_user, text="Ваш запрос на права администратора отклонен"
        )
