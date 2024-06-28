from aiogram import Bot, F, Router, filters, types
from aiogram.fsm.context import FSMContext
from dishka import AsyncContainer

from application.common.states import UpdateFile
from application.usecases.callbacks.update_db_data import UpdateDatabaseDataCallback
from application.usecases.commands.update_db_data import UpdateDatabaseDataCommand
from application.usecases.users.get_user import GetAllAdmins
from application.usecases.users.update_user import DemoteUser, PromoteUserToAdmin
from domain.common.response import Response
from presentation.common.keyboards import update_category_keyboard
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
        return await get_admins_interactor(message=message)


@admin_router.message(filters.Command("update_info"))
async def cmd_update_info(message: types.Message, state: FSMContext):
    await state.set_state(UpdateFile.category)
    await message.answer(
        "Выберите какую информацию нужно обновить",
        reply_markup=types.InlineKeyboardMarkup(
            inline_keyboard=update_category_keyboard
        ),
    )


@admin_router.message(filters.Command("promote_user"))
async def cmd_promote_user(
    message: types.Message,
    container: AsyncContainer,
    command: filters.command.CommandObject,
):
    async with container() as di_container:
        promote_user_interactor = await di_container.get(PromoteUserToAdmin)
        return await promote_user_interactor(message=message, command=command)


@admin_router.message(filters.Command("demote_user"))
async def cmd_demote_user(
    message: types.Message,
    container: AsyncContainer,
    command: filters.command.CommandObject,
):
    async with container() as di_container:
        demote_user_interactor = await di_container.get(DemoteUser)
        return await demote_user_interactor(message=message, command=command)


@admin_router.callback_query(UpdateFile.category, F.data.startswith("update_"))
async def callback_update_info(
    callback: types.CallbackQuery,
    state: FSMContext,
    container: AsyncContainer,
):
    async with container() as di_container:
        get_admins_interactor = await di_container.get(UpdateDatabaseDataCallback)
        return await get_admins_interactor(callback=callback, state=state)


@admin_router.message(UpdateFile.file)
async def upload_file(
    message: types.Message, bot: Bot, state: FSMContext, container: AsyncContainer
):
    async with container() as di_container:
        update_db_data_interactor = await di_container.get(UpdateDatabaseDataCommand)
        await update_db_data_interactor(message=message, state=state, bot=bot)
