from dataclasses import dataclass

from domain.admins.admin import Admin
from domain.admins.repository import BaseAdminRepository


@dataclass
class CreateAdmin:
    admin_repository: BaseAdminRepository

    async def __call__(self, user_id: int, username: str = "") -> Admin:
        user_exists = await self.admin_repository.get_by_id(user_id)
        if user_exists:
            return "Пользователь уже администратор"

        user = Admin.create(telegram_id=user_id, username=username)
        await self.admin_repository.create(user.telegram_id)

        return user
