import asyncio

from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from sqlalchemy import text
from sqlalchemy.ext.asyncio import AsyncEngine

from infrastructure.config import settings
from infrastructure.di.container import get_container, init_logger
from infrastructure.persistence.models.base import Base
from presentation.routers.admin import admin_router
from presentation.routers.search import search_router


def init_routers(dp: Dispatcher):
    dp.include_router(admin_router)
    dp.include_router(search_router)


async def init_head_admin(conn):
    try:
        await conn.execute(
            text(
                "INSERT INTO admins (telegram_id, role) VALUES ({0}, 'head')".format(
                    settings.HEAD_ADMIN_TG_ID
                )
            )
        )
    except Exception as e:
        print(e)


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
    engine = await container.get(AsyncEngine)
    async with engine.begin() as conn:
        # await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)
        await init_head_admin(conn)
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
