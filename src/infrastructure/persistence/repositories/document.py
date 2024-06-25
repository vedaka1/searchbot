from dataclasses import dataclass

from sqlalchemy import text
from sqlalchemy.ext.asyncio import AsyncSession

from domain.documents.document import Document
from domain.documents.repository import BaseDocumentRepository
from domain.employees.employe import Employe
from domain.employees.repository import BaseEmployeRepository


@dataclass
class DocumentRepository(BaseDocumentRepository):

    __slots__ = ("session",)
    session: AsyncSession

    async def create(self) -> None: ...

    async def delete(self, id: int) -> None: ...

    async def get_by_search_prompt(
        self, search_prompt: str, limit: int = 10, offset: int = 0
    ) -> list[Employe]:
        query = text(
            """
            SELECT * FROM documents
            WHERE documents.credentials ILIKE '%:search_prompt%' or documents.name ILIKE '%:search_prompt%'
            LIMIT :limit OFFSET :offset;
            """
        )
        result = await self.session.execute(
            query, {"search_prompt": search_prompt, "limit": limit, "offset": offset}
        )
        result = result.mappings().all()
        return [Document(**data) for data in result]

    async def get_by_id(self, id: int) -> None: ...

    async def get_all(self, limit: int = 10, offset: int = 0) -> list[Employe]: ...

    async def update(self) -> None: ...
