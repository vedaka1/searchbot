from dataclasses import dataclass

import pandas as pd
from sqlalchemy import Engine


@dataclass
class CreateAllDocuments:
    engine: Engine

    def __call__(self, file) -> None:
        df = pd.read_excel(file, header=2)
        document_columns = [
            "id",
            "department",
            "document_type",
            "first_publishing",
            "publishing_date",
            "lvl_1",
            "queue_1",
            "lvl_2",
            "queue_2",
            "lvl_3",
            "queue_3",
            "lvl_4",
            "queue_4",
            "credentials",
            "title",
            "link_text",
        ]
        try:
            df.columns = document_columns
            df.to_sql(name="documents", con=self.engine, if_exists="replace")

        except ValueError:
            return "Количество столбцов в файле не совпадает со столбцами в базе данных"
        except Exception as e:
            print(e)
            return "Не удалось обновить информацию"
