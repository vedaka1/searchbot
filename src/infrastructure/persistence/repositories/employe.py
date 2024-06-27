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

    async def create(self) -> None:
        pass

    async def delete(self, id: int) -> None:
        pass

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

    async def get_by_id(self, id: int) -> None:
        pass

    async def get_all(self, limit: int = 10, offset: int = 0) -> list[Employe]:
        pass

    async def update(self) -> None:
        pass
