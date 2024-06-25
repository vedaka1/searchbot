from dataclasses import dataclass
from typing import Any

import pandas as pd
from sqlalchemy import Engine


@dataclass
class CreateAllEmployees:
    engine: Engine

    def __call__(self, file) -> None:
        df = pd.read_excel(file)
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

        except ValueError:
            return "Количество столбцов в файле не совпадает со столбцами в базе данных"
        except Exception as e:
            print(e)
            return "Не удалось обновить информацию"
