from typing import Any, Awaitable, Callable, Dict

from aiogram import BaseMiddleware
from aiogram.types import TelegramObject

from application.usecases.users.get_user import GetAdminByTelegramId
from infrastructure.config import settings
from infrastructure.di.container import get_container
from presentation.texts.text import text


class AdminMiddleware(BaseMiddleware):
    async def __call__(
        self,
        handler: Callable[[TelegramObject, Dict[str, Any]], Awaitable[Any]],
        event: TelegramObject,
        data: Dict[str, Any],
    ) -> Any:
        user = data["event_from_user"]
        container = get_container()
        if user.id == settings.HEAD_ADMIN_TG_ID:
            return await handler(event, data)
        async with container() as di_container:
            get_admin = await di_container.get(GetAdminByTelegramId)
            admin = await get_admin(user.id)
            if admin is None:
                return await event.answer(text["permission_denied"])
        return await handler(event, data)
