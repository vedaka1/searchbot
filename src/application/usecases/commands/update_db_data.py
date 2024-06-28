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

    def __call__(self, category: str, destination_path: str) -> str:
        repository = {
            "Вебсайт": self.website_repository,
            "Документ": self.document_repository,
            "Сотрудник": self.employe_repository,
        }

        if category not in repository:
            return "Неверная категория"

        try:
            repository[category].excel_to_db(
                engine=self.engine, destination_path=destination_path
            )
        except ValueError as e:
            self.logger.error("usecase: UpdateDatabaseData error: {0}".format(e))
            return "Количество столбцов в файле не совпадает со столбцами в базе данных"

        except Exception as e:
            self.logger.error("usecase: UpdateDatabaseData error: {0}".format(e))
            return "Не удалось обновить информацию"

        return "Данные успешно загружены"
