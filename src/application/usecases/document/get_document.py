from dataclasses import dataclass, field

from openpyxl import load_workbook

from application.common.workbook import DocumentWorkbook
from domain.common.response import Response


@dataclass
class GetDocument:
    wb: DocumentWorkbook
    _ignored_symbols: list = field(
        default=[None, "", "@", "-", "9999999"],
        init=False,
    )

    def __call__(self, search_prompt: str) -> str:

        ws = self.wb.active
        search_prompt = search_prompt.lower()
        result = ""
        name = ""
        search_columns = ws["N":"O"]

        try:
            for cell in tuple(zip(search_columns[0], search_columns[1])):
                if (
                    search_prompt in str(cell[0].value).lower()
                    or search_prompt in str(cell[1].value).lower()
                ):
                    result += "\n"
                    row = ws[cell[0].row]
                    cells_to_parse = (1, 5, 7, 9, 11)
                    for cell_number in cells_to_parse:
                        if row[cell_number].value not in self._ignored_symbols:
                            result += f"{row[cell_number].value}\n"

                    credentials = "*Реквизиты*: {0}".format(row[13].value)
                    name = "*Название*: [{0}]({1})".format(row[14].value, row[15].value)
                    date = "*Дата*: {0}".format(row[4].value)
                    result += "{0}\n{1}\n".format(credentials, date)

        except Exception as e:
            print(e)
            return "Записей не найдено"
        if not result:
            return "Записей не найдено"

        result = Response(result).value
        result += name

        if len(result) > 4000:
            return result[:4000] + "\.\.\."
        return result
