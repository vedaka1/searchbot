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
        user = await self.admin_repository.get_by_telegram_id(user_id)
        if user is None:
            return None
        return user
