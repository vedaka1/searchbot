from dataclasses import dataclass

from sqlalchemy import text
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
        self, search_prompt: str, limit: int = 10, offset: int = 0
    ) -> list[Employe]:
        try:
            query = text(
                """
                SELECT * FROM employees
                WHERE employees.lastname ILIKE :search_prompt or employees.firstname_patronymic ILIKE :search_prompt
                LIMIT :limit OFFSET :offset;
                """
            )
            result = await self.session.execute(
                query,
                {
                    "search_prompt": str("%" + search_prompt + "%"),
                    "limit": limit,
                    "offset": offset,
                },
            )
            result = result.mappings().all()
            return [Employe(**data) for data in result]
        except Exception as e:
            print(e)
            return None

    async def get_by_id(self, id: int) -> None:
        pass

    async def get_all(self, limit: int = 10, offset: int = 0) -> list[Employe]:
        pass

    async def update(self) -> None:
        pass
