import uuid
from dataclasses import dataclass

from sqlalchemy import text
from sqlalchemy.ext.asyncio import AsyncSession

from domain.admins.admin import Admin
from domain.admins.repository import BaseAdminRepository


@dataclass
class AdminRepository(BaseAdminRepository):

    __slots__ = ("session",)
    session: AsyncSession

    async def create(self, user: Admin) -> None:
        query = text(
            """
                INSERT INTO admins (id, telegram_id, username)
                VALUES (:id, :telegram_id, :username)
            """
        )
        await self.session.execute(
            query,
            {
                "id": user.id,
                "telegram_id": user.telegram_id,
                "username": user.username,
            },
        )
        return None

    async def delete(self, telegram_id: int) -> None:
        query = text(
            """
                DELETE FROM admins
                WHERE telegram_id = :value;
                """
        )
        await self.session.execute(
            query,
            {
                "value": telegram_id,
            },
        )
        return None

    async def get_by_telegram_id(self, telegram_id: int) -> Admin:
        query = text("""SELECT * FROM admins WHERE telegram_id = :value;""")
        result = await self.session.execute(query, {"value": telegram_id})
        result = result.mappings().one_or_none()
        if result is None:
            return None

        return Admin(**result)

    async def get_by_id(self, user_id: uuid.UUID) -> Admin:
        query = text("""SELECT * FROM admins WHERE id = :value;""")
        result = await self.session.execute(query, {"value": user_id})
        result = result.mappings().one_or_none()
        if result is None:
            return None

        return Admin(**result)

    async def get_all(self, limit: int = 10, offset: int = 0) -> list[Admin]:
        query = text("""SELECT * FROM admins LIMIT :limit OFFSET :offset;""")
        result = await self.session.execute(query, {"limit": limit, "offset": offset})
        result = result.mappings().all()
        return [Admin(**data) for data in result]
