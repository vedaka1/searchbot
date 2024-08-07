from dataclasses import dataclass
from logging import Logger

from domain.common.response import Response
from domain.websites.repository import BaseWebsiteRepository


@dataclass
class GetWebsite:
    """A class that returns all websites matching the search prompt"""

    website_repository: BaseWebsiteRepository
    logger: Logger

    async def __call__(self, message_text: str) -> str:
        try:
            search_prompt = "%" + r"%%".join(list(message_text.split())) + "%"
            websites = await self.website_repository.get_by_search_prompt(
                search_prompt=search_prompt
            )
            count = await self.website_repository.get_count(search_prompt=search_prompt)
        except Exception as e:
            self.logger.error("usecase: GetWebsite error: {0}".format(e))
            return "Возникла ошибка"

        if not websites:
            return "Записей о вебсайтах не найдено"

        result = "Найдено записей: {0}\n".format(count)
        separator = "<-------->\n"
        for key, website in enumerate(websites):
            website_body = separator
            for atr in website.__dict__:
                if website.__dict__[atr] in (None, "", "@", "9999999"):
                    website.__dict__[atr] = ""

            website_body += "{0}\n{1}\n".format(
                website.long_name,
                website.short_name,
            )
            if website.contacts_1:
                website_body += "*Контакт 1:* {0}\n".format(website.contacts_1)
            if website.contacts_2:
                website_body += "*Контакт 2:* {0}\n".format(website.contacts_2)

            website_body = Response(website_body).value
            website_body += "\n[{0}](https://{1})\n".format(
                Response(website.domain).value, website.domain
            )

            if len(result) + len(website_body) > 4000:
                result += "\nОтображено записей {0}/{1}".format(key + 1, len(websites))
                return result

            result += website_body

        return result
