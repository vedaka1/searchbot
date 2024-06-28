from dataclasses import dataclass
from logging import Logger

from aiogram import types

from domain.common.response import Response
from domain.websites.repository import BaseWebsiteRepository


@dataclass
class GetWebsite:
    """A class that returns all employees matching the search prompt"""

    website_repository: BaseWebsiteRepository
    logger: Logger

    async def __call__(self, message: types.Message) -> str:
        try:
            search_prompt = "%" + r"%%".join(list(message.text.split())) + "%"
            websites = await self.website_repository.get_by_search_prompt(
                search_prompt=search_prompt
            )
        except Exception as e:
            self.logger.error("usecase: GetWebsite error: {0}".format(e))
            return await message.answer("Возникла ошибка")

        if not websites:
            return await message.answer("Записей о вебсайтах не найдено")

        result = "Найдено записей: {0}\n".format(len(websites))
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
                return await message.answer(result, parse_mode="MarkDownV2")

            result += website_body

        return await message.answer(result, parse_mode="MarkDownV2")
