from dataclasses import dataclass, field

from openpyxl import load_workbook

from application.common.workbook import DocumentWorkbook
from domain.common.response import Response


@dataclass
class GetDocument:

    async def __call__(self, search_prompt: str) -> str:

        return result
