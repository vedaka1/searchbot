from dataclasses import dataclass
from logging import Logger

from aiogram import Bot, types
from aiogram.fsm.context import FSMContext
from sqlalchemy import Engine

from domain.documents.repository import BaseDocumentRepository
from domain.employees.repository import BaseEmployeRepository
from domain.websites.repository import BaseWebsiteRepository


@dataclass
class UpdateDatabaseDataCommand:
    website_repository: BaseWebsiteRepository
    document_repository: BaseDocumentRepository
    employe_repository: BaseEmployeRepository
    engine: Engine
    logger: Logger

    async def __call__(
        self, message: types.Message, state: FSMContext, bot: Bot
    ) -> str:
        repository = {
            "Вебсайт": self.website_repository,
            "Документ": self.document_repository,
            "Сотрудник": self.employe_repository,
        }
        data = await state.get_data()
        category = data.get("category")
        file_id = message.document.file_id
        file_info = await bot.get_file(file_id)
        file_path = file_info.file_path
        if not file_path.endswith(".xlsx"):
            return await message.answer("Файл должен быть в формате .xlsx")

        destination_path = "infrastructure/excel/data.xlsx"
        await bot.download_file(file_path, destination=destination_path)

        if category not in repository:
            return await message.answer("Неверная категория")

        try:
            repository[category].excel_to_db(
                engine=self.engine, destination_path=destination_path
            )
        except ValueError as e:
            self.logger.error("usecase: UpdateDatabaseData error: {0}".format(e))
            return await message.answer(
                "Количество столбцов в файле не совпадает со столбцами в базе данных"
            )
        except Exception as e:
            self.logger.error("usecase: UpdateDatabaseData error: {0}".format(e))
            return await message.answer("Не удалось обновить информацию")

        await message.answer("Данные успешно загружены")
        await state.clear()
