from dataclasses import dataclass
from logging import Logger
from typing import Any

from aiogram import Bot, types
from aiogram.fsm.context import FSMContext

from application.common.admin import HeadAdminID
from application.common.transaction import BaseTransactionManager
from domain.common.response import Response
from domain.users.repository import BaseUserRepository
from domain.users.user import User


@dataclass
class RequestAccessCommand:
    user_repository: BaseUserRepository
    transaction_manager: BaseTransactionManager
    head_admin_id: HeadAdminID
    logger: Logger

    async def __call__(
        self,
        message: types.Message,
        bot: Bot,
        state: FSMContext,
    ) -> Any:

        await state.clear()
        user_id = str(message.from_user.id)
        username = message.from_user.username
        head_admin_id = self.head_admin_id

        user = await self.user_repository.get_by_id(user_id)
        if user:
            if user.role == "admin":
                return await message.answer("У вас уже есть права администратора")
        else:
            user = User.create(telegram_id=user_id, username=username)
            try:
                await self.user_repository.create(user)
                await self.transaction_manager.commit()
            except Exception as e:
                self.logger.error("usecase: CreateUser error: {0}".format(e))

        text = Response(
            "Пользователь запросил права администратора\n\n*ID:* {0}\n*username:* {1}".format(
                message.from_user.id, message.from_user.username
            )
        ).value
        await bot.send_message(
            chat_id=head_admin_id,
            text=text,
            reply_markup=types.InlineKeyboardMarkup(
                inline_keyboard=[
                    [
                        types.InlineKeyboardButton(
                            text="Принять",
                            callback_data=f"requestAccess_accept_{user_id}",
                        )
                    ],
                    [
                        types.InlineKeyboardButton(
                            text="Отказать",
                            callback_data=f"requestAccess_reject_{user_id}",
                        )
                    ],
                ]
            ),
            parse_mode="MarkDownV2",
        )
        await message.answer("Запрос отправлен")
