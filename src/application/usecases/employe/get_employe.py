from dataclasses import dataclass
from logging import Logger

from domain.common.response import Response
from domain.employees.repository import BaseEmployeRepository


@dataclass
class GetEmploye:
    """A class that returns all employees matching the search prompt"""

    employe_repository: BaseEmployeRepository
    logger: Logger

    async def __call__(self, message_text: str) -> str:
        try:
            search_prompt = "%" + r"%%".join(list(message_text.split())) + "%"
            employes = await self.employe_repository.get_by_search_prompt(
                search_prompt=search_prompt
            )
            count = await self.employe_repository.get_count(search_prompt=search_prompt)
        except Exception as e:
            self.logger.error("usecase: GetEmploye error: {0}".format(e))
            return "Возникла ошибка"

        if not employes:
            return "Записей о сотрудниках не найдено"

        result = "Найдено записей: {0}\n".format(count)
        separator = "<-------->\n"
        for key, employe in enumerate(employes):
            employe_body = separator
            for atr in employe.__dict__:
                if employe.__dict__[atr] in (None, "@", "9999999"):
                    employe.__dict__[atr] = ""

            for workplace in (
                employe.lvl_1_office,
                employe.lvl_2_management,
                employe.lvl_3_department,
                employe.lvl_4_reserve,
            ):
                if workplace:
                    employe_body += workplace + "\n"

            employe_body += (
                "*Должность:* {0}\n*ФИО:* {1} {2}\n*Номер:* ({3}){4}\n".format(
                    employe.position,
                    employe.lastname,
                    employe.firstname_patronymic,
                    int(employe.phone_code),
                    employe.phone_number,
                )
            )
            if employe.email:
                employe_body += "*Почта:* {0}\n".format(employe.email)
            employe_body = Response(employe_body).value

            if len(result) + len(employe_body) > 4000:
                result += "\nОтображено записей {0}/{1}".format(key + 1, len(employes))
                return result

            result += employe_body

        return result
