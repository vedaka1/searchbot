from aiogram import Bot, F, Router, filters, types
from aiogram.fsm.context import FSMContext
from dishka import AsyncContainer

from application.common.states import UpdateFile
from application.usecases.commands.update_db_data import UpdateDatabaseDataCommand
from application.usecases.users.get_user import GetAllAdmins
from application.usecases.users.update_user import DemoteUser, PromoteUserToAdmin
from domain.common.response import Response
from presentation.common.keyboards import kb
from presentation.middlewares.admin import AdminMiddleware
from presentation.texts.text import text

admin_router = Router()
admin_router.message.middleware(AdminMiddleware())


@admin_router.message(filters.Command("info"))
async def cmd_info(message: types.Message):
    await message.answer(Response(text.info).value, parse_mode="MarkDownV2")


@admin_router.message(filters.Command("admins"))
async def cmd_admins(message: types.Message, container: AsyncContainer):
    async with container() as di_container:
        get_admins_interactor = await di_container.get(GetAllAdmins)
        result = await get_admins_interactor()
        await message.answer(Response(result).value, parse_mode="MarkDownV2")


@admin_router.message(filters.Command("update_info"))
async def cmd_update_info(message: types.Message, state: FSMContext):
    await state.set_state(UpdateFile.category)
    await message.answer(
        "Выберите какую информацию нужно обновить",
        reply_markup=types.InlineKeyboardMarkup(
            inline_keyboard=kb.update_category_keyboard()
        ),
    )


@admin_router.message(filters.Command("promote_user"))
async def cmd_promote_user(
    message: types.Message,
    container: AsyncContainer,
    command: filters.command.CommandObject,
):
    async with container() as di_container:
        user_id = command.args
        if not user_id:
            await message.answer("Укажите id пользователя через пробел после команды")
        promote_user_interactor = await di_container.get(PromoteUserToAdmin)
        result = await promote_user_interactor(int(user_id.split()[0]))
        await message.answer(result)


@admin_router.message(filters.Command("demote_user"))
async def cmd_demote_user(
    message: types.Message,
    container: AsyncContainer,
    command: filters.command.CommandObject,
):
    async with container() as di_container:
        demote_user_interactor = await di_container.get(DemoteUser)
        result = await demote_user_interactor(command.args)
        await message.answer(result)


@admin_router.callback_query(UpdateFile.category, F.data.startswith("update_"))
async def callback_update_info(
    callback: types.CallbackQuery,
    state: FSMContext,
):
    user_choice = callback.data.split("_")[1]
    choices = {
        "Сотрудник": "Отправьте файл с сотрудниками в формате .xlsx",
        "Документ": "Отправьте файл с документами в формате .xlsx",
        "Вебсайт": "Отправьте файл с вебсайтами в формате .xlsx",
    }
    await state.update_data(category=user_choice)
    await state.set_state(UpdateFile.file)
    return await callback.message.edit_text(choices[user_choice])


@admin_router.message(
    UpdateFile.file,
    F.content_type.in_({"document"}),
)
async def upload_file(
    message: types.Message, bot: Bot, state: FSMContext, container: AsyncContainer
):
    async with container() as di_container:
        data = await state.get_data()
        category = data.get("category")
        file_id = message.document.file_id
        file_info = await bot.get_file(file_id)
        file_path = file_info.file_path
        if not file_path.endswith(".xlsx"):
            return await message.answer("Файл должен быть в формате .xlsx")
        destination_path = "infrastructure/excel/data.xlsx"
        await bot.download_file(file_path, destination=destination_path)
        update_db_data_interactor = await di_container.get(UpdateDatabaseDataCommand)
        result = await update_db_data_interactor(category, destination_path)
        await message.answer(result)
        await state.clear()
