from abc import ABC, abstractmethod
from dataclasses import dataclass

from sqlalchemy import Engine

from domain.websites.website import Website


@dataclass
class BaseWebsiteRepository(ABC):
    """An abstract webiste repository for their implementations"""

    @abstractmethod
    async def get_by_search_prompt(
        self, search_prompt: str, limit: int = 100, offset: int = 0
    ) -> list[Website]: ...

    @abstractmethod
    async def get_count(self, search_prompt: str) -> int: ...

    @abstractmethod
    def excel_to_db(self, engine: Engine, destination_path: str) -> None: ...
