from abc import ABC, abstractmethod
from dataclasses import dataclass

from domain.users.user import User


@dataclass
class BaseUserRepository(ABC):
    """An abstract user repository for their implementations"""

    @abstractmethod
    async def create(self, user: User) -> None: ...

    @abstractmethod
    async def delete(self, telegram_id: int) -> None: ...

    @abstractmethod
    async def get_by_id(self, telegram_id: int) -> User: ...

    @abstractmethod
    async def get_admin_by_id(self, telegram_id: int) -> User: ...

    @abstractmethod
    async def get_all(self, limit: int = 10, offset: int = 0) -> list[User]: ...

    @abstractmethod
    async def update_role(self, user: User) -> None: ...
