from dataclasses import dataclass
from logging import Logger
from typing import Any

from aiogram import Bot, types

from application.common.transaction import BaseTransactionManager
from domain.users.repository import BaseUserRepository


@dataclass
class RequestAccessCallback:
    user_repository: BaseUserRepository
    transaction_manager: BaseTransactionManager
    logger: Logger

    async def __call__(
        self,
        callback: types.CallbackQuery,
        bot: Bot,
    ) -> Any:
        user_choice = callback.data.split("_")[1]
        from_user = int(callback.data.split("_")[2])
        if user_choice == "accept":

            user = await self.user_repository.get_by_id(from_user)
            user.role = "admin"
            await self.user_repository.update_role(user)

            await callback.message.delete()
            await bot.send_message(
                chat_id=from_user,
                text="Ваш запрос на права администратора был одобрен",
            )
        if user_choice == "reject":
            await callback.message.delete()
            await bot.send_message(
                chat_id=from_user, text="Ваш запрос на права администратора отклонен"
            )
        await self.transaction_manager.commit()
