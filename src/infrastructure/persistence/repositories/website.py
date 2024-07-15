from dataclasses import dataclass

import pandas as pd
from sqlalchemy import Engine, text
from sqlalchemy.ext.asyncio import AsyncSession

from domain.websites.repository import BaseWebsiteRepository
from domain.websites.website import Website


@dataclass
class WebsiteRepository(BaseWebsiteRepository):

    __slots__ = ("session",)
    session: AsyncSession

    async def get_by_search_prompt(
        self, search_prompt: str, limit: int = 100, offset: int = 0
    ) -> list[Website]:
        query = text(
            """
            SELECT * FROM websites
            WHERE websites.long_name ILIKE :search_prompt
            or websites.short_name ILIKE :search_prompt
            or websites.domain ILIKE :search_prompt
            LIMIT :limit OFFSET :offset;
            """
        )
        result = await self.session.execute(
            query,
            {
                "search_prompt": search_prompt,
                "limit": limit,
                "offset": offset,
            },
        )
        result = result.mappings().all()
        return [Website(**data) for data in result]

    async def get_count(self, search_prompt: str) -> int:
        query = text(
            """
            SELECT COUNT(*) FROM websites
            WHERE websites.long_name ILIKE :search_prompt
            or websites.short_name ILIKE :search_prompt
            or websites.domain ILIKE :search_prompt
            """
        )
        result = await self.session.execute(
            query,
            {"search_prompt": str("%" + search_prompt + "%")},
        )
        return result.scalar_one()

    def excel_to_db(self, engine: Engine, destination_path: str) -> None:
        df: pd.DataFrame = pd.read_excel(destination_path)
        employe_columns = [
            "long_name",
            "short_name",
            "domain",
            "contacts_1",
            "contacts_2",
        ]

        df.columns = employe_columns
        df.to_sql(name="websites", con=engine, if_exists="replace")
