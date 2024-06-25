from abc import ABC, abstractmethod
from dataclasses import dataclass

from domain.employees.employe import Employe


@dataclass
class BaseEmployeRepository(ABC):
    @abstractmethod
    async def create(self) -> None: ...

    @abstractmethod
    async def delete(self, id: int) -> None: ...

    @abstractmethod
    async def get_by_search_prompt(self, search_prompt: str) -> list[Employe]: ...

    @abstractmethod
    async def get_by_id(self, id: int) -> Employe: ...

    @abstractmethod
    async def get_all(self, limit: int = 10, offset: int = 0) -> list[Employe]: ...

    @abstractmethod
    async def update(self) -> None: ...
