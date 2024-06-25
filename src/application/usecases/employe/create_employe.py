from dataclasses import dataclass
from typing import Any

import pandas as pd


@dataclass
class CreateAllEmployees:

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
        df.columns = employe_columns
