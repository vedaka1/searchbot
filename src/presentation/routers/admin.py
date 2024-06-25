from aiogram import Bot, F, Router, filters, types
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from dishka import AsyncContainer

from application.usecases.admin.create_admin import CreateAdmin
from application.usecases.admin.get_admin import GetHeadAdmin
from application.usecases.document.create_document import CreateAllDocuments
from application.usecases.employe.create_employe import CreateAllEmployees
from domain.admins.admin import Admin
from presentation.common.keyboards import category_keyboard, request_access_keyboard
from presentation.middlewares.admin import AdminMiddleware
from presentation.texts.text import text

admin_router = Router()
admin_router.message.middleware(AdminMiddleware())


class UpdateFile(StatesGroup):
    category = State()
    file = State()


@admin_router.message(filters.Command("info"))
async def start(message: types.Message):
    await message.answer(text["admin"])


@admin_router.message(filters.Command("update_info"))
async def search(message: types.Message, state: FSMContext):
    await state.set_state(UpdateFile.category)
    await message.answer(
        "Выберите какую информацию нужно обновить",
        reply_markup=types.InlineKeyboardMarkup(inline_keyboard=category_keyboard),
    )


@admin_router.callback_query(UpdateFile.category, F.data.startswith("search_"))
async def select_subscription_callback(
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


@admin_router.message(UpdateFile.file)
async def select_subscription_callback(
    message: types.Message, state: FSMContext, bot: Bot, container: AsyncContainer
):
    file_id = message.document.file_id
    file_info = await bot.get_file(file_id)
    file_path = file_info.file_path

    data = await state.get_data()
    category = data.get("category")
    if category == "Сотрудник":
        async with container() as di_container:
            destination_path = "infrastructure/excel/employees_data.xlsx"
            await bot.download_file(file_path, destination=destination_path)
            update_employe = await di_container.get(CreateAllEmployees)
            update_employe(destination_path)

            await message.answer("Информация успешно обновлена")
            await state.clear()

    if category == "Документ":
        async with container() as di_container:
            destination_path = "infrastructure/excel/documents_data.xlsx"
            await bot.download_file(file_path, destination=destination_path)
            update_employe = await di_container.get(CreateAllDocuments)
            update_employe(destination_path)

            await message.answer("Информация успешно обновлена")
            await state.clear()


@admin_router.message(filters.Command("request_access"))
async def search(message: types.Message, bot: Bot, container: AsyncContainer):
    async with container() as di_container:
        get_head_admin = await di_container.get(GetHeadAdmin)
        head_admin: Admin = await get_head_admin()
    await bot.send_message(
        chat_id=head_admin.telegram_id,
        text=f"Пользователь запросил права администратора\n\n*ID:* {message.from_user.id}\n*sername:* {message.from_user.username}\n*firstname:* {message.from_user.first_name}\n*lastname:* {message.from_user.last_name}",
        reply_markup=types.InlineKeyboardMarkup(
            inline_keyboard=request_access_keyboard(message.from_user.id)
        ),
        parse_mode="MarkDownV2",
    )
    await message.answer("Запрос отправлен")


@admin_router.callback_query(F.data.startswith("requestAccess_"))
async def search(
    callback: types.CallbackQuery,
    bot: Bot,
    container: AsyncContainer,
):
    user_choice = callback.data.split("_")[1]
    from_user = callback.data.split("_")[2]
    if user_choice == "accept":
        async with container() as di_container:
            create_admin = await di_container.get(CreateAdmin)
            await create_admin(int(from_user))
            await callback.message.delete()
            await bot.send_message(
                chat_id=from_user, text="Ваш запрос на права администратора был одобрен"
            )
    if user_choice == "reject":
        await callback.message.delete()
        await bot.send_message(
            chat_id=from_user, text="Ваш запрос на права администратора отклонен"
        )
