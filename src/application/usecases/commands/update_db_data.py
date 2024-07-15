import asyncio
from concurrent.futures import ThreadPoolExecutor
from dataclasses import dataclass
from logging import Logger

from sqlalchemy import Engine

from domain.documents.repository import BaseDocumentRepository
from domain.employees.repository import BaseEmployeRepository
from domain.websites.repository import BaseWebsiteRepository
from domain.common.enums import Categories


@dataclass
class UpdateDatabaseDataCommand:
    website_repository: BaseWebsiteRepository
    document_repository: BaseDocumentRepository
    employe_repository: BaseEmployeRepository
    engine: Engine
    logger: Logger

    async def __call__(self, category: str, destination_path: str) -> str:
        repository: dict[str, BaseEmployeRepository] = {
            Categories.EMPLOYE.value: self.employe_repository,
            Categories.DOCUMENT.value: self.document_repository,
            Categories.WEBSITE.value: self.website_repository,
        }
        if category not in repository:
            return "Неверная категория"

        lock = asyncio.Lock()
        await lock.acquire()
        try:
            with ThreadPoolExecutor() as executor:
                await asyncio.get_event_loop().run_in_executor(
                    executor,
                    repository[category].excel_to_db,
                    self.engine,
                    destination_path,
                )
        except ValueError as e:
            self.logger.error("usecase: UpdateDatabaseData error: {0}".format(e))
            return "Количество столбцов в файле не совпадает со столбцами в базе данных"

        except Exception as e:
            self.logger.error("usecase: UpdateDatabaseData error: {0}".format(e))
            return "Не удалось обновить информацию"

        finally:
            lock.release()
            return "Данные успешно загружены"
