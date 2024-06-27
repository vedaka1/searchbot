from dataclasses import dataclass
from typing import Any

from aiogram import types
from aiogram.fsm.context import FSMContext

from application.common.states import UpdateFile


@dataclass
class UpdateInfo:

    async def __call__(
        self,
        callback: types.CallbackQuery,
        state: FSMContext,
    ) -> Any:
        user_choice = callback.data.split("_")[1]
        await state.update_data(category=user_choice)
        await state.set_state(UpdateFile.file)
        if user_choice == "Сотрудник":
            return await callback.message.edit_text(
                "Отправьте файл с сотрудниками в формате .xlsx"
            )
        if user_choice == "Документ":
            return await callback.message.edit_text(
                "Отправьте файл с документами в формате .xlsx"
            )
