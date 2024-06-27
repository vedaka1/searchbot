from dataclasses import dataclass
from logging import Logger

import pandas as pd
from aiogram import Bot, types
from sqlalchemy import Engine


@dataclass
class CreateAllEmployees:
    engine: Engine
    logger: Logger

    async def __call__(self, message: types.Message, bot: Bot) -> str:
        file_id = message.document.file_id
        file_info = await bot.get_file(file_id)
        file_path = file_info.file_path
        if not file_path.endswith(".xlsx"):
            return await message.answer("Файл должен быть в формате .xlsx")

        destination_path = "infrastructure/excel/employees_data.xlsx"
        await bot.download_file(file_path, destination=destination_path)

        df = pd.read_excel(destination_path)
        employe_columns = [
            "lvl_0_deputy",
            "link_to_deputy",
            "lvl_1_office",
            "link_to_office",
            "lvl_2_management",
            "queue_lvl_2",
            "link_to_management",
            "lvl_3_department",
            "queue_lvl_3",
            "link_to_department",
            "lvl_4_reserve",
            "link_to_reserve",
            "queue",
            "lastname",
            "firstname_patronymic",
            "link",
            "position",
            "cabinet_number",
            "phone_code",
            "phone_number",
            "phone_number_2",
            "internal_number",
            "fax",
            "email",
        ]
        try:
            df.columns = employe_columns
            df.to_sql(name="employees", con=self.engine, if_exists="replace")
            return await message.answer("Данные успешно обновлены")

        except ValueError as e:
            self.logger.error("usecase: CreateAllEmployees error: {0}".format(e))
            return await message.answer(
                "Количество столбцов в файле не совпадает со столбцами в базе данных"
            )
        except Exception as e:
            self.logger.error("usecase: CreateAllEmployees error: {0}".format(e))
            return await message.answer("Не удалось обновить информацию")
