from logging import getLogger

from aiogram import Bot, F, Router, filters, types
from aiogram.fsm.context import FSMContext
from dishka import AsyncContainer

from application.common.states import Search
from application.usecases.document.get_document import GetDocument
from application.usecases.employe.get_employe import GetEmploye
from application.usecases.users.create_user import CreateUser
from application.usecases.users.get_user import GetUserByTelegramId
from application.usecases.users.update_user import PromoteUserToAdmin
from application.usecases.websites.get_website import GetWebsite
from domain.common.response import Response
from infrastructure.config import settings
from presentation.common.keyboards import kb
from presentation.texts.text import text

logger = getLogger()
search_router = Router()


@search_router.message(filters.Command("request_access"))
async def cmd_request_access(
    message: types.Message,
    bot: Bot,
    state: FSMContext,
    container: AsyncContainer,
    users: list,
):
    async with container() as di_container:
        await state.clear()
        user_id = message.from_user.id
        username = message.from_user.username
        if user_id in users:
            return await message.answer("Вы уже отправили запрос")
        get_admin_interactor = await di_container.get(GetUserByTelegramId)
        user = await get_admin_interactor(user_id, username)
        if user.role == "admin":
            return await message.answer("У вас уже есть права администратора")
        users.append(user_id)
        await bot.send_message(
            chat_id=settings.HEAD_ADMIN_TG_ID,
            text=Response(text.request_access(user_id, username)).value,
            reply_markup=types.InlineKeyboardMarkup(
                inline_keyboard=kb.request_access_keyboard(user_id)
            ),
            parse_mode="MarkDownV2",
        )
        await message.answer("Запрос отправлен")


@search_router.callback_query(F.data.startswith("requestAccess_"))
async def callback_request_access(
    callback: types.CallbackQuery, bot: Bot, container: AsyncContainer, users: list
):
    async with container() as di_container:
        user_choice = callback.data.split("_")[1]
        from_user = int(callback.data.split("_")[2])
        if user_choice == "accept":
            request_access_callback_interactor = await di_container.get(
                PromoteUserToAdmin
            )
            result = await request_access_callback_interactor(from_user)
            await callback.message.answer(result)
            await bot.send_message(
                chat_id=from_user,
                text="Ваш запрос на права администратора был одобрен",
            )
        if user_choice == "reject":
            await bot.send_message(
                chat_id=from_user, text="Ваш запрос на права администратора отклонен"
            )
        users.remove(from_user)
        await callback.message.delete()


@search_router.message(filters.Command("start"))
async def cmd_start(message: types.Message, container: AsyncContainer):
    async with container() as di_container:
        create_user = await di_container.get(CreateUser)
        await create_user(message.from_user.id, message.from_user.username)
        await message.answer(text.start)


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
            inline_keyboard=kb.search_category_keyboard()
        ),
    )


@search_router.callback_query(Search.category, F.data.startswith("search_"))
async def callback_search(
    callback: types.CallbackQuery,
    state: FSMContext,
):
    user_choice = callback.data.split("_")[1]
    await state.update_data(category=user_choice)
    categories = {
        "Сотрудник": "Введите ФИО или должность сотрудника",
        "Документ": "Введите название или реквизиты документа",
        "Вебсайт": "Введите название, домен или ИОГВ вебсайта",
    }
    await callback.message.edit_text(categories[user_choice])


@search_router.message(Search.category)
async def search(message: types.Message, container: AsyncContainer, state: FSMContext):
    await state.set_state(Search.search)
    data = await state.get_data()
    category = data.get("category")
    categories = {
        "Сотрудник": GetEmploye,
        "Документ": GetDocument,
        "Вебсайт": GetWebsite,
    }
    async with container() as di_container:
        get_item_interactor = await di_container.get(categories[category])
        result = await get_item_interactor(message.text)
        await message.answer(result, parse_mode="MarkDownV2")
        await state.clear()
