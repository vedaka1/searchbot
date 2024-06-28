from dataclasses import dataclass
from typing import Any

from aiogram import types
from aiogram.fsm.context import FSMContext

from application.common.states import UpdateFile


@dataclass
class UpdateDatabaseDataCallback:

    async def __call__(
        self,
        callback: types.CallbackQuery,
        state: FSMContext,
    ) -> Any:
        user_choice = callback.data.split("_")[1]
        choices = {
            "Сотрудник": "Отправьте файл с сотрудниками в формате .xlsx",
            "Документ": "Отправьте файл с документами в формате .xlsx",
            "Вебсайт": "Отправьте файл с вебсайтами в формате .xlsx",
        }
        await state.update_data(category=user_choice)
        await state.set_state(UpdateFile.file)
        return await callback.message.edit_text(choices[user_choice])
