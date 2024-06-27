from aiogram import Bot, F, Router, filters, types
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from dishka import AsyncContainer

from application.usecases.document.create_document import CreateAllDocuments
from application.usecases.employe.create_employe import CreateAllEmployees
from application.usecases.users.get_user import GetAllAdmins
from application.usecases.users.update_user import DemoteUser, PromoteUserToAdmin
from domain.common.response import Response
from presentation.common.keyboards import category_keyboard
from presentation.middlewares.admin import AdminMiddleware
from presentation.texts.text import text

admin_router = Router()
admin_router.message.middleware(AdminMiddleware())


class UpdateFile(StatesGroup):
    category = State()
    file = State()


@admin_router.message(filters.Command("info"))
async def cmd_info(message: types.Message):
    await message.answer(Response(text["info"]).value, parse_mode="MarkDownV2")


@admin_router.message(filters.Command("admins"))
async def cmd_info(message: types.Message, container: AsyncContainer):
    async with container() as di_container:
        get_admins = await di_container.get(GetAllAdmins)
        admins = await get_admins()
        result = "Список администраторов:\n"
        for admin in admins:
            result += " - id: `{0}` username: {1}\n".format(
                admin.telegram_id, admin.username
            )
        await message.answer(Response(result).value, parse_mode="MarkDownV2")


@admin_router.message(filters.Command("update_info"))
async def cmd_update_info(message: types.Message, state: FSMContext):
    await state.set_state(UpdateFile.category)
    await message.answer(
        "Выберите какую информацию нужно обновить",
        reply_markup=types.InlineKeyboardMarkup(inline_keyboard=category_keyboard),
    )


@admin_router.message(filters.Command("promote_user"))
async def cmd_update_info(
    message: types.Message,
    container: AsyncContainer,
    command: filters.command.CommandObject,
):
    user_id = command.args
    if not user_id:
        return await message.answer(
            "Укажите id пользователя через пробел после команды"
        )
    async with container() as di_container:
        promote_user = await di_container.get(PromoteUserToAdmin)
        result = await promote_user(int(user_id.split()[0]))
        await message.answer(result)


@admin_router.message(filters.Command("demote_user"))
async def cmd_update_info(
    message: types.Message,
    container: AsyncContainer,
    command: filters.command.CommandObject,
):
    user_id = command.args
    if not user_id:
        return await message.answer(
            "Укажите id пользователя через пробел после команды"
        )
    async with container() as di_container:
        demote_user = await di_container.get(DemoteUser)
        result = await demote_user(int(user_id.split()[0]))
        await message.answer(result)


@admin_router.callback_query(UpdateFile.category)
async def callback_search(
    callback: types.CallbackQuery,
    state: FSMContext,
):
    user_choice = callback.data.split("_")[1]
    await state.update_data(category=user_choice)
    await state.set_state(UpdateFile.file)
    if user_choice == "Сотрудник":
        await callback.message.edit_text(
            "Отправьте файл с сотрудниками в формате .xlsx"
        )
    if user_choice == "Документ":
        await callback.message.edit_text("Отправьте файл с документами в формате .xlsx")


@admin_router.message(UpdateFile.file, F)
async def upload_file(
    message: types.Message, state: FSMContext, bot: Bot, container: AsyncContainer
):
    file_id = message.document.file_id
    file_info = await bot.get_file(file_id)
    file_path = file_info.file_path
    if not file_path.endswith(".xlsx"):
        return await message.answer("Файл должен быть в формате .xlsx")

    data = await state.get_data()
    category = data.get("category")
    async with container() as di_container:
        if category == "Сотрудник":
            destination_path = "infrastructure/excel/employees_data.xlsx"
            await bot.download_file(file_path, destination=destination_path)
            update_employe = await di_container.get(CreateAllEmployees)
            result = update_employe(destination_path)

            await message.answer(result)
            await state.clear()

        if category == "Документ":
            destination_path = "infrastructure/excel/documents_data.xlsx"
            await bot.download_file(file_path, destination=destination_path)
            update_document = await di_container.get(CreateAllDocuments)
            result = update_document(destination_path)

            await message.answer(result)
            await state.clear()
