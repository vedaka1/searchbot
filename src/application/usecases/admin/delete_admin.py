from dataclasses import dataclass
from logging import Logger

from application.common.transaction import BaseTransactionManager
from domain.admins.repository import BaseAdminRepository


@dataclass
class DeleteAdmin:
    admin_repository: BaseAdminRepository
    transaction_manager: BaseTransactionManager
    logger: Logger

    async def __call__(self, user_id: int) -> None:
        try:
            await self.admin_repository.delete(user_id)
        except Exception as e:
            self.logger.error("usecase: DeleteAdmin error: {0}".format(e))
            return None

        await self.transaction_manager.commit()
        return None
