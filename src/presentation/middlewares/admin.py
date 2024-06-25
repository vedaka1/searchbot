from typing import Any, Awaitable, Callable, Dict

from aiogram import BaseMiddleware
from aiogram.types import TelegramObject

from application.usecases.admin.get_admin import GetAdminByTelegramId
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
        async with container() as di_container:
            get_admin = await di_container.get(GetAdminByTelegramId)
            admin = await get_admin(user.id)
            if admin is None:
                return await event.answer(text["permission_denied"], show_alert=True)
        return await handler(event, data)
