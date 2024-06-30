from abc import ABC, abstractmethod
from dataclasses import dataclass

from sqlalchemy import Engine

from domain.employees.employe import Employe


@dataclass
class BaseEmployeRepository(ABC):
    """An abstract employe repository for their implementations"""

    @abstractmethod
    async def get_by_search_prompt(
        self, search_prompt: str, limit: int = 100, offset: int = 0
    ) -> list[Employe]: ...

    @abstractmethod
    def excel_to_db(self, engine: Engine, destination_path: str) -> None: ...
