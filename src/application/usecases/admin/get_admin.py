from dataclasses import dataclass

from domain.admins.admin import Admin
from domain.admins.repository import BaseAdminRepository


@dataclass
class GetAllAdmins:
    admin_repository: BaseAdminRepository

    async def __call__(self) -> list[Admin]:
        result = await self.admin_repository.get_all()
        return result


@dataclass
class GetAdminByTelegramId:
    admin_repository: BaseAdminRepository

    async def __call__(self, user_id: int) -> Admin | None:
        user = await self.admin_repository.get_by_id(user_id)
        if user is None:
            return None
        return user


@dataclass
class GetHeadAdmin:
    admin_repository: BaseAdminRepository

    async def __call__(self) -> Admin | None:
        users = await self.admin_repository.get_all()
        if not users:
            return None
        for user in users:
            if user.role == "head":
                return user
            else:
                return None
