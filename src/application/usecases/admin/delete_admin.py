from dataclasses import dataclass

from domain.admins.repository import BaseAdminRepository


@dataclass
class DeleteAdmin:
    admin_repository: BaseAdminRepository

    async def __call__(self, user_id: int) -> None:
        await self.admin_repository.delete(user_id)
        return None
