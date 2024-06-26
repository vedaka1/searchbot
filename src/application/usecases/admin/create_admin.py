from dataclasses import dataclass
from logging import Logger

from application.common.transaction import BaseTransactionManager
from domain.admins.admin import Admin
from domain.admins.repository import BaseAdminRepository


@dataclass
class CreateAdmin:
    admin_repository: BaseAdminRepository
    transaction_manager: BaseTransactionManager
    logger: Logger

    async def __call__(self, user_id: int, username: str = "") -> Admin:
        user_exists = await self.admin_repository.get_by_id(user_id)
        if user_exists:
            return "Пользователь уже администратор"

        user = Admin.create(telegram_id=user_id, username=username)
        print(user)
        try:
            await self.admin_repository.create(user)
        except Exception as e:
            self.logger.error("usecase: CreateAdmin error: {0}".format(e))
            return "Ошибка при создании пользователя"

        await self.transaction_manager.commit()
        return user
