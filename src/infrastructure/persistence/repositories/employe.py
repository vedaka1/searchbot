from dataclasses import dataclass

import pandas as pd
from sqlalchemy import Engine, text
from sqlalchemy.ext.asyncio import AsyncSession

from domain.employees.employe import Employe
from domain.employees.repository import BaseEmployeRepository


@dataclass
class EmployeRepository(BaseEmployeRepository):

    __slots__ = ("session",)
    session: AsyncSession

    async def get_by_search_prompt(
        self, search_prompt: str, limit: int = 100, offset: int = 0
    ) -> list[Employe]:
        query = text(
            """
            SELECT * FROM employees
            WHERE CONCAT(employees.lastname, ' ', employees.firstname_patronymic) ILIKE :search_prompt
            or CONCAT(employees.firstname_patronymic, ' ', employees.lastname) ILIKE :search_prompt
            or employees.position ILIKE :search_prompt
            LIMIT :limit OFFSET :offset;
            """
        )
        result = await self.session.execute(
            query,
            {
                "search_prompt": search_prompt,
                "limit": limit,
                "offset": offset,
            },
        )
        result = result.mappings().all()
        return [Employe(**data) for data in result]

    async def get_count(self, search_prompt: str) -> int:
        query = text(
            """
            SELECT COUNT(*) FROM employees
            WHERE CONCAT(employees.lastname, ' ', employees.firstname_patronymic) ILIKE :search_prompt
            or CONCAT(employees.firstname_patronymic, ' ', employees.lastname) ILIKE :search_prompt
            or employees.position ILIKE :search_prompt
            """
        )
        result = await self.session.execute(
            query,
            {"search_prompt": str("%" + search_prompt + "%")},
        )
        return result.scalar_one()

    def excel_to_db(self, engine: Engine, destination_path: str) -> None:
        df: pd.DataFrame = pd.read_excel(destination_path)
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
        df.to_sql(name="employees", con=engine, if_exists="replace")
