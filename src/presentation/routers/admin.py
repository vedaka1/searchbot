from aiogram import Bot, F, Router, filters, types
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from dishka import AsyncContainer

from application.usecases.document.create_document import CreateAllDocuments
from application.usecases.employe.create_employe import CreateAllEmployees
from presentation.common.keyboards import category_keyboard, request_access_keyboard
from presentation.middlewares.admin import AdminMiddleware
from presentation.texts.text import text

admin_router = Router()
admin_router.message.middleware(AdminMiddleware())


class UpdateFile(StatesGroup):
    category = State()
    file = State()


@admin_router.message(filters.Command("info"))
async def cmd_info(message: types.Message):
    await message.answer(text["admin"])


@admin_router.message(filters.Command("update_info"))
async def cmd_update_info(message: types.Message, state: FSMContext):
    await state.set_state(UpdateFile.category)
    await message.answer(
        "Выберите какую информацию нужно обновить",
        reply_markup=types.InlineKeyboardMarkup(inline_keyboard=category_keyboard),
    )


@admin_router.callback_query(UpdateFile.category, F.data.startswith("search_"))
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


@admin_router.message(UpdateFile.file)
async def upload_file(
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
            try:
                update_employe(destination_path)
            except ValueError:
                return await message.answer(
                    "Количество столбцов в файле не совпадает со столбцами в базе данных"
                )
            except:
                return await message.answer("Возникла ошибка")
            finally:
                await state.clear()

            await message.answer("Информация успешно обновлена")
