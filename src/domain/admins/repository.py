import uuid
from abc import ABC, abstractmethod
from dataclasses import dataclass

from domain.admins.admin import Admin


@dataclass
class BaseAdminRepository(ABC):
    @abstractmethod
    async def create(self, user: Admin) -> None: ...

    @abstractmethod
    async def delete(self, telegram_id: int) -> None: ...

    @abstractmethod
    async def get_by_id(self, user_id: uuid.UUID) -> Admin: ...

    @abstractmethod
    async def get_all(self, limit: int = 10, offset: int = 0) -> list[Admin]: ...
