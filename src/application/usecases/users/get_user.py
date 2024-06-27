from dataclasses import dataclass

from aiogram import types

from application.common.admin import HeadAdminID
from domain.common.response import Response
from domain.users.repository import BaseUserRepository
from domain.users.user import User


@dataclass
class GetAllUsers:
    user_repository: BaseUserRepository

    async def __call__(self) -> list[User]:
        result = await self.user_repository.get_all()
        return result


@dataclass
class GetAdminByTelegramId:
    user_repository: BaseUserRepository

    async def __call__(self, user_id: int) -> User | None:
        try:
            user = await self.user_repository.get_admin_by_id(user_id)
            if user is None:
                return None
            return user
        except:
            return None


@dataclass
class GetHeadAdminId:
    head_admin_id: HeadAdminID

    async def __call__(self) -> str:
        return self.head_admin_id


@dataclass
class GetAllAdmins:
    user_repository: BaseUserRepository

    async def __call__(self, message: types.Message) -> list[User]:
        admins_list = await self.user_repository.get_all()
        admins = [user for user in admins_list if user.role == "admin"]

        result = "Список администраторов:\n"
        for admin in admins:
            result += " - id: `{0}` username: {1}\n".format(
                admin.telegram_id, admin.username
            )
        await message.answer(Response(result).value, parse_mode="MarkDownV2")
