from dataclasses import dataclass
from logging import Logger

from sqlalchemy import Engine

from domain.websites.repository import BaseWebsiteRepository


@dataclass
class UpdateWebsites:
    website_repository: BaseWebsiteRepository
    engine: Engine
    logger: Logger

    async def __call__(self, destination_path: str) -> str:
        self.website_repository.pandas_to_db(destination_path)
