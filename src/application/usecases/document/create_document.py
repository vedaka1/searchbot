from dataclasses import dataclass
from logging import Logger

import pandas as pd
from aiogram import Bot, types
from sqlalchemy import Engine


@dataclass
class CreateAllDocuments:
    engine: Engine
    logger: Logger

    async def __call__(self, message: types.Message, bot: Bot) -> str:
        file_id = message.document.file_id
        file_info = await bot.get_file(file_id)
        file_path = file_info.file_path
        if not file_path.endswith(".xlsx"):
            return await message.answer("Файл должен быть в формате .xlsx")

        destination_path = "infrastructure/excel/documents_data.xlsx"
        await bot.download_file(file_path, destination=destination_path)

        df = pd.read_excel(destination_path, header=2)
        document_columns = [
            "id",
            "department",
            "document_type",
            "first_publishing",
            "publishing_date",
            "lvl_1",
            "queue_1",
            "lvl_2",
            "queue_2",
            "lvl_3",
            "queue_3",
            "lvl_4",
            "queue_4",
            "credentials",
            "title",
            "link_text",
        ]
        try:
            df.columns = document_columns
            df.to_sql(name="documents", con=self.engine, if_exists="replace")
            return await message.answer("Данные успешно обновлены")

        except ValueError:
            self.logger.error("usecase: CreateAllDocuments error: {0}".format(e))
            return await message.answer(
                "Количество столбцов в файле не совпадает со столбцами в базе данных"
            )
        except Exception as e:
            self.logger.error("usecase: CreateAllDocuments error: {0}".format(e))
            return await message.answer("Не удалось обновить информацию")
