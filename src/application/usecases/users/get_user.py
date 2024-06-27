from dataclasses import dataclass

from application.common.admin import HeadAdminID
from domain.users.repository import BaseUserRepository
from domain.users.user import User


@dataclass
class GetAllUsers:
    user_repository: BaseUserRepository

    async def __call__(self) -> list[User]:
        result = await self.user_repository.get_all()
        return result


@dataclass
class GetAdminByTelegramId:
    user_repository: BaseUserRepository

    async def __call__(self, user_id: int) -> User | None:
        user = await self.user_repository.get_admin_by_id(user_id)
        if user is None:
            return None
        return user


@dataclass
class GetHeadAdminId:
    head_admin_id: HeadAdminID

    async def __call__(self) -> int:
        return self.head_admin_id


@dataclass
class GetAllAdmins:
    user_repository: BaseUserRepository

    async def __call__(self) -> list[User]:
        result = await self.user_repository.get_all()
        result = [user for user in result if user.role == "admin"]
        return result
