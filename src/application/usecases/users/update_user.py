from dataclasses import dataclass
from logging import Logger

from application.common.transaction import BaseTransactionManager
from domain.users.repository import BaseUserRepository
from domain.users.user import User


@dataclass
class UpdateUserRole:
    user_repository: BaseUserRepository
    transaction_manager: BaseTransactionManager
    logger: Logger

    async def __call__(self, user_id: int) -> User:
        user = await self.user_repository.get_by_id(user_id)
        if not user:
            return

        if user.role == "admin":
            return

        try:
            user.role = "admin"
            await self.user_repository.update_role(user)
        except Exception as e:
            self.logger.error("usecase: UpdateUserRole error: {0}".format(e))
            return

        await self.transaction_manager.commit()
        return user
