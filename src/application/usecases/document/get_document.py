from dataclasses import dataclass, field

from domain.common.response import Response
from domain.documents.repository import BaseDocumentRepository


@dataclass
class GetDocument:
    document_repository: BaseDocumentRepository

    async def __call__(self, search_prompt: str) -> str:
        documents = await self.document_repository.get_by_search_prompt(
            search_prompt=search_prompt, limit=100
        )
        print(documents)
        if not documents:
            return "Записей о документах не найдено"
        result = "Найдено записей: {0}\n".format(len(documents))
        separator = "<-------->\n"
        for key, document in enumerate(documents):
            document_body = separator
            for atr in document.__dict__:
                if document.__dict__[atr] in (None, "", "@", "9999999"):
                    document.__dict__[atr] = ""

            workplace = ""
            for place in (
                document.department,
                document.lvl_1,
                document.lvl_2,
                document.lvl_3,
                document.lvl_4,
            ):
                if place:
                    workplace += place + "\n"
            document_body += workplace

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
                document_body += "[Ссылка]({0})\n".format(document.link_text)
            if len(result) + len(document_body) > 4000:
                result += "\nОтображено записей {0}/{1}".format(key + 1, len(documents))
                return result

            result += document_body

        if not result:
            return "Записей не найдено"

        return result
