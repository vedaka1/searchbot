from dataclasses import dataclass

import pandas as pd
from sqlalchemy import Engine, text
from sqlalchemy.ext.asyncio import AsyncSession

from domain.documents.document import Document
from domain.documents.repository import BaseDocumentRepository


@dataclass
class DocumentRepository(BaseDocumentRepository):

    __slots__ = ("session",)
    session: AsyncSession

    async def get_by_search_prompt(
        self, search_prompt: str, limit: int = 100, offset: int = 0
    ) -> list[Document]:
        query = text(
            """
            SELECT * FROM documents
            WHERE documents.credentials ILIKE :search_prompt or documents.title ILIKE :search_prompt
            LIMIT :limit OFFSET :offset;
            """
        )
        result = await self.session.execute(
            query,
            {
                "search_prompt": str("%" + search_prompt + "%"),
                "limit": limit,
                "offset": offset,
            },
        )
        result = result.mappings().all()
        return [Document(**data) for data in result]

    async def get_count(self, search_prompt: str) -> int:
        query = text(
            """
            SELECT COUNT(*) FROM documents
            WHERE documents.credentials ILIKE :search_prompt or documents.title ILIKE :search_prompt
            """
        )
        result = await self.session.execute(
            query,
            {"search_prompt": str("%" + search_prompt + "%")},
        )
        return result.scalar_one()

    def excel_to_db(self, engine: Engine, destination_path: str) -> None:
        df: pd.DataFrame = pd.read_excel(destination_path, header=2)
        document_columns = [
            "id",
            "department",
            "document_type",
            "first_publishing",
            "publishing_date",
            "lvl_1",
            "queue_1",
            "lvl_2",
            "queue_2",
            "lvl_3",
            "queue_3",
            "lvl_4",
            "queue_4",
            "credentials",
            "title",
            "link_text",
        ]
        df.columns = document_columns
        df.to_sql(name="documents", con=engine, if_exists="replace")
