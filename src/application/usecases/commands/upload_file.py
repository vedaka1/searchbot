from dataclasses import dataclass
from logging import Logger
from typing import Any

from aiogram import Bot, types
from aiogram.fsm.context import FSMContext
from sqlalchemy import Engine

from domain.documents.repository import BaseDocumentRepository
from domain.employees.repository import BaseEmployeRepository


@dataclass
class UploadFile:
    document_repository: BaseDocumentRepository
    employe_repository: BaseEmployeRepository
    engine: Engine
    logger: Logger

    async def __call__(
        self,
        message: types.Message,
        state: FSMContext,
        bot: Bot,
    ) -> Any:
        file_id = message.document.file_id
        file_info = await bot.get_file(file_id)
        file_path = file_info.file_path
        if not file_path.endswith(".xlsx"):
            return await message.answer("Файл должен быть в формате .xlsx")

        data = await state.get_data()
        category = data.get("category")
        result = ""
        try:
            if category == "Документ":
                destination_path = "infrastructure/excel/documents_data.xlsx"
                await bot.download_file(file_path, destination=destination_path)
                result = self.document_repository.update_documents_with_pandas(
                    self.engine, destination_path
                )

            if category == "Сотрудник":
                destination_path = "infrastructure/excel/employees_data.xlsx"
                await bot.download_file(file_path, destination=destination_path)
                result = self.employe_repository.update_employees_with_pandas(
                    self.engine, destination_path
                )

        except ValueError:
            self.logger.error("usecase: UploadFile error: {0}".format(e))
            await state.clear()
            return message.answer(
                "Количество столбцов в файле не совпадает со столбцами в базе данных"
            )
        except Exception as e:
            self.logger.error("usecase: UploadFile error: {0}".format(e))
            await state.clear()
            return message.answer("Не удалось обновить информацию")

        await state.clear()
        await message.answer(result)
