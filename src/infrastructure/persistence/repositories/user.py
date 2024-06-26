from dataclasses import dataclass

from sqlalchemy import text
from sqlalchemy.ext.asyncio import AsyncSession

from domain.users.repository import BaseUserRepository
from domain.users.user import User


@dataclass
class UserRepository(BaseUserRepository):

    __slots__ = ("session",)
    session: AsyncSession

    async def create(self, user: User) -> None:
        query = text(
            """
                INSERT INTO users (telegram_id, username, role)
                VALUES (:telegram_id, :username, :role)
            """
        )
        await self.session.execute(
            query,
            {
                "telegram_id": user.telegram_id,
                "username": user.username,
                "role": user.role,
            },
        )
        return None

    async def delete(self, telegram_id: int) -> None:
        query = text(
            """
                DELETE FROM users
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

    async def get_by_id(self, telegram_id: int) -> User | None:
        query = text("""SELECT * FROM users WHERE telegram_id = :value;""")
        result = await self.session.execute(query, {"value": telegram_id})
        result = result.mappings().one_or_none()
        if result is None:
            return None

        return User(**result)

    async def get_admin_by_id(self, telegram_id: int) -> User | None:
        query = text(
            """SELECT * FROM users WHERE telegram_id = :value and role = 'admin';"""
        )
        result = await self.session.execute(query, {"value": telegram_id})
        result = result.mappings().one_or_none()
        if result is None:
            return None

        return User(**result)

    async def get_all(self, limit: int = 10, offset: int = 0) -> list[User]:
        query = text("""SELECT * FROM users LIMIT :limit OFFSET :offset;""")
        result = await self.session.execute(query, {"limit": limit, "offset": offset})
        result = result.mappings().all()
        return [User(**data) for data in result]

    async def update_role(self, user: User) -> None:
        query = text(
            """
                UPDATE users
                SET role = :role
                WHERE telegram_id = :telegram_id;
            """
        )
        await self.session.execute(
            query,
            {"telegram_id": user.telegram_id, "role": user.role},
        )
        return None
