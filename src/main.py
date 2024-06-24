import asyncio

from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode

from infrastructure.config import settings
from infrastructure.di.container import get_container, init_logger
from presentation.routers.search import search_router


def init_routers(dp: Dispatcher):
    dp.include_router(search_router)


async def main():
    init_logger()
    bot = Bot(
        token=settings.BOT_TOKEN,
        default=DefaultBotProperties(parse_mode=ParseMode.HTML),
    )
    dp = Dispatcher()
    init_routers(dp)
    container = get_container()
    dp["container"] = container
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
