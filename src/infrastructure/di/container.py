import logging
from functools import lru_cache
from typing import AsyncGenerator

from dishka import AsyncContainer, Provider, Scope, make_async_container, provide
from sqlalchemy import Engine
from sqlalchemy.ext.asyncio import AsyncEngine, AsyncSession, async_sessionmaker

from application.common.admin import HeadAdminID
from application.common.transaction import BaseTransactionManager
from application.usecases.document.create_document import CreateAllDocuments
from application.usecases.document.get_document import GetDocument
from application.usecases.employe.create_employe import CreateAllEmployees
from application.usecases.employe.get_employe import GetEmploye
from application.usecases.users import *
from domain.documents.repository import BaseDocumentRepository
from domain.employees.repository import BaseEmployeRepository
from domain.users.repository import BaseUserRepository
from infrastructure.config import settings
from infrastructure.persistence.main import (
    create_session_factory,
    get_async_engine,
    get_sync_engine,
)
from infrastructure.persistence.repositories.document import DocumentRepository
from infrastructure.persistence.repositories.employe import EmployeRepository
from infrastructure.persistence.repositories.user import UserRepository
from infrastructure.persistence.transaction import TransactionManager


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
    def async_engine(self) -> AsyncEngine:
        return get_async_engine()

    @provide(scope=Scope.APP)
    def sync_engine(self) -> Engine:
        return get_sync_engine()

    @provide(scope=Scope.APP)
    def logger(self) -> logging.Logger:
        return logging.getLogger()

    @provide(scope=Scope.APP)
    def session_factory(self, engine: AsyncEngine) -> async_sessionmaker:
        return create_session_factory(engine)

    @provide(scope=Scope.APP)
    def head_admin(self) -> HeadAdminID:
        return settings.HEAD_ADMIN_TG_ID


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
    user_repository = provide(UserRepository, provides=BaseUserRepository)
    transaction_manager = provide(TransactionManager, provides=BaseTransactionManager)


class UseCasesProvider(Provider):
    scope = Scope.REQUEST

    get_employe = provide(GetEmploye)
    get_document = provide(GetDocument)
    get_user_by_id = provide(GetAdminByTelegramId)
    get_users = provide(GetAllUsers)
    get_admins = provide(GetAllAdmins)
    delete_user = provide(DeleteUser)
    create_user = provide(CreateUser)
    promote_user = provide(PromoteUserToAdmin)
    demote_user = provide(DemoteUser)
    create_employees = provide(CreateAllEmployees)
    create_documents = provide(CreateAllDocuments)
    get_head_admin = provide(GetHeadAdminId)


@lru_cache(1)
def get_container() -> AsyncContainer:
    return make_async_container(
        UseCasesProvider(),
        DatabaseAdaptersProvider(),
        DatabaseConfigurationProvider(),
        SettingsProvider(),
    )
