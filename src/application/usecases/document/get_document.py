from dataclasses import dataclass
from logging import Logger

from domain.common.response import Link, Response
from domain.documents.repository import BaseDocumentRepository


@dataclass
class GetDocument:
    """A class that returns all documents matching the search prompt"""

    document_repository: BaseDocumentRepository
    logger: Logger

    async def __call__(self, message_text: str) -> str:
        try:
            search_prompt = "%" + r"%%".join(list(message_text.split())) + "%"
            documents = await self.document_repository.get_by_search_prompt(
                search_prompt=search_prompt
            )
            count = await self.document_repository.get_count(
                search_prompt=search_prompt
            )
        except Exception as e:
            self.logger.error("usecase: GetDocument error: {0}".format(e))
            return "Возникла ошибка"

        if not documents:
            return "Записей о документах не найдено"

        result = "Найдено записей: {0}\n".format(count)
        separator = "<-------->\n"
        for key, document in enumerate(documents):
            document_body = separator
            for atr in document.__dict__:
                if document.__dict__[atr] in (None, "@", "9999999"):
                    document.__dict__[atr] = ""

            for workplace in (
                document.department,
                document.lvl_1,
                document.lvl_2,
                document.lvl_3,
                document.lvl_4,
            ):
                if workplace:
                    document_body += workplace + "\n"

            document_body += (
                "*Тип:* {0}\n*Реквизиты:* {1}\n*Название:* {2}\n*Дата:* {3}\n".format(
                    document.document_type,
                    document.credentials,
                    document.title,
                    document.publishing_date,
                )
            )
            document_body = Response(document_body).value
            if document.link_text:
                document_body += "[Ссылка]({0})\n".format(
                    Link(document.link_text).value
                )

            if len(result) + len(document_body) > 4000:
                result += "\nОтображено записей {0}/{1}".format(key + 1, len(documents))
                return result

            result += document_body

        return result
