from dataclasses import dataclass, field

from application.common.workbook import EmployeWorkbook
from domain.common.response import Response
from domain.employees.repository import BaseEmployeRepository


@dataclass
class GetEmploye:
    employe_repository: BaseEmployeRepository

    async def __call__(self, search_prompt: str) -> str:
        employes = await self.employe_repository.get_by_search_prompt(
            search_prompt=search_prompt
        )
        if employes is None:
            return "Записей не найдено"
        result = ""
        separator = "--------\n"
        for employe in employes:
            result += separator
            for atr in employe.__dict__:
                if employe.__dict__[atr] in (None, "", "@", "9999999"):
                    employe.__dict__[atr] = ""

            workplace = ""
            for place in (
                employe.lvl_1_office,
                employe.lvl_2_management,
                employe.lvl_3_department,
                employe.lvl_4_reserve,
            ):
                if place:
                    workplace += place + "\n"
            result += workplace

            result += "{0}\n*ФИО:* {1} {2}\n*Номер:* ({3}){4}\n".format(
                employe.position,
                employe.lastname,
                employe.firstname_patronymic,
                int(employe.phone_code),
                employe.phone_number,
            )
            if employe.email:
                result += "*Почта:* {0}\n".format(employe.email)

        return Response(result).value
