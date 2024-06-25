import logging
from functools import lru_cache
from typing import AsyncGenerator

from dishka import AsyncContainer, Provider, Scope, make_async_container, provide
from openpyxl import load_workbook
from sqlalchemy.ext.asyncio import AsyncEngine, AsyncSession, async_sessionmaker

from application.usecases.admin import *
from application.usecases.document.get_document import GetDocument
from application.usecases.employe.get_employe import GetEmploye
from domain.admins.repository import BaseAdminRepository
from domain.documents.repository import BaseDocumentRepository
from domain.employees.repository import BaseEmployeRepository
from infrastructure.config import settings
from infrastructure.persistence.main import create_engine, create_session_factory
from infrastructure.persistence.repositories.admin import AdminRepository
from infrastructure.persistence.repositories.document import DocumentRepository
from infrastructure.persistence.repositories.employe import EmployeRepository


@lru_cache(1)
def init_logger() -> logging.Logger:
    logging.basicConfig(
        # filename="log.log",
        level=logging.INFO,
        encoding="UTF-8",
        format="%(asctime)s %(levelname)s: %(message)s",
    )


class SettingsProvider(Provider):
    @provide(scope=Scope.APP)
    def engine(self) -> AsyncEngine:
        return create_engine()

    @provide(scope=Scope.APP)
    def session_factory(self, engine: AsyncEngine) -> async_sessionmaker:
        return create_session_factory(engine)


class DatabaseConfigurationProvider(Provider):
    @provide(scope=Scope.REQUEST, provides=AsyncSession)
    async def provide_db_connection(
        self, session_factory: async_sessionmaker
    ) -> AsyncGenerator[AsyncSession, None]:
        session = session_factory()
        yield session
        await session.close()


class DatabaseAdaptersProvider(Provider):
    scope = Scope.REQUEST

    employe_repository = provide(EmployeRepository, provides=BaseEmployeRepository)
    document_repository = provide(DocumentRepository, provides=BaseDocumentRepository)
    admin_repository = provide(AdminRepository, provides=BaseAdminRepository)


class UseCasesProvider(Provider):
    scope = Scope.REQUEST

    get_employe = provide(GetEmploye)
    get_document = provide(GetDocument)
    get_admin_by_id = provide(GetAdminByTelegramId)
    get_admins = provide(GetAllAdmins)
    delete_admin = provide(DeleteAdmin)
    create_admin = provide(CreateAdmin)


@lru_cache(1)
def get_container() -> AsyncContainer:
    return make_async_container(
        UseCasesProvider(),
        DatabaseAdaptersProvider(),
        DatabaseConfigurationProvider(),
        SettingsProvider(),
    )
