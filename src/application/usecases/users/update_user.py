from dataclasses import dataclass
from logging import Logger

from aiogram import filters, types

from application.common.transaction import BaseTransactionManager
from domain.users.repository import BaseUserRepository


@dataclass
class PromoteUserToAdmin:
    user_repository: BaseUserRepository
    transaction_manager: BaseTransactionManager
    logger: Logger

    async def __call__(
        self,
        message: types.Message,
        command: filters.command.CommandObject,
    ) -> None:
        user_id = command.args
        if not user_id:
            return await message.answer(
                "Укажите id пользователя через пробел после команды"
            )

        user = await self.user_repository.get_by_id(int(user_id.split()[0]))
        if not user:
            return await message.answer("Пользователь не найден")

        if user.role == "admin":
            return await message.answer("Пользователь уже имеет права администратора")

        try:
            user.role = "admin"
            await self.user_repository.update_role(user)
        except Exception as e:
            self.logger.error("usecase: UpdateUserRole error: {0}".format(e))
            return await message.answer("Возникла ошибка")

        await self.transaction_manager.commit()
        return await message.answer(
            f"Пользователь {user.telegram_id} теперь имеет права администратора"
        )


@dataclass
class DemoteUser:
    user_repository: BaseUserRepository
    transaction_manager: BaseTransactionManager
    logger: Logger

    async def __call__(
        self,
        message: types.Message,
        command: filters.command.CommandObject,
    ) -> str:
        user_id = command.args
        if not user_id:
            return await message.answer(
                "Укажите id пользователя через пробел после команды"
            )

        user = await self.user_repository.get_by_id(int(user_id.split()[0]))
        if not user:
            return await message.answer("Пользователь не найден")

        if user.role == "user":
            return await message.answer(
                f"Пользователь {user.telegram_id} понижен в правах"
            )

        try:
            user.role = "user"
            await self.user_repository.update_role(user)
        except Exception as e:
            self.logger.error("usecase: UpdateUserRole error: {0}".format(e))
            return await message.answer("Возникла ошибка")

        await self.transaction_manager.commit()
        return await message.answer(f"Пользователь {user.telegram_id} понижен в правах")
