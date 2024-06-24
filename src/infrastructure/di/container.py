import logging
from functools import lru_cache

from dishka import (
    AsyncContainer,
    Provider,
    Scope,
    from_context,
    make_async_container,
    provide,
)
from openpyxl import load_workbook

from application.common.workbook import DocumentWorkbook, EmployeWorkbook
from application.usecases.document.get_document import GetDocument
from application.usecases.employe.get_employe import GetEmploye
from infrastructure.config import settings


@lru_cache(1)
def init_logger() -> logging.Logger:
    logging.basicConfig(
        # filename="log.log",
        level=logging.INFO,
        encoding="UTF-8",
        format="%(asctime)s %(levelname)s: %(message)s",
    )


class UseCasesProvider(Provider):
    scope = Scope.APP

    get_employe = provide(GetEmploye)
    get_document = provide(GetDocument)


class WorkbookProvider(Provider):
    @provide(scope=Scope.APP)
    def employe_workbook(self) -> EmployeWorkbook:
        return load_workbook(
            "infrastructure/excel/ПФ_Телефонный_справочник_Телефонный_справочник_без_доп_символов.xlsx"
        )

    @provide(scope=Scope.APP)
    def document_workbook(self) -> DocumentWorkbook:
        return load_workbook(
            "infrastructure/excel/ПФ_Справочник_документов_Справочник_документов_АгПечСМИ15.xlsx"
        )


@lru_cache(1)
def get_container() -> AsyncContainer:
    return make_async_container(
        WorkbookProvider(),
        UseCasesProvider(),
    )
