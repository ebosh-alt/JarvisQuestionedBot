import datetime
from typing import Literal, TYPE_CHECKING, Union

import gspread
import pytz
from google.oauth2.service_account import Credentials
from gspread import Worksheet
from loguru import logger

from internal.entities.models import Participants

if TYPE_CHECKING:
    from internal.entities.database import User

TypeObjectDB = Union["User",]

SCOPES = [
    "https://www.googleapis.com/auth/spreadsheets",
    "https://www.googleapis.com/auth/drive",
]

NAMED_TABLE = "JarvisQuestionedBot"

NAMED_SHEET = Literal[
    "users"
]

INDEXES_COLUMNS = {
    1: "A",
    2: "B",
    3: "C",
    4: "D",
    5: "E",
    6: "F",
    7: "G",
    8: "H",
}
SERVICE_ACCOUNT_FILE = "config/service_account.json"
MOSCOW_TZ = pytz.timezone("Europe/Moscow")


class Client:
    """
    Класс для работы с Google Sheets API.
    """

    def __init__(self, service_account_file: str, scopes: list):
        """
        Инициализация клиента Google Sheets API.

        :param service_account_file: Путь к файлу с учетными данными сервисного аккаунта.
        :param scopes: Список областей доступа.
        """
        self.__creds = Credentials.from_service_account_file(
            service_account_file, scopes=scopes
        )
        self.__client = gspread.authorize(self.__creds)

    def __get_worksheet(self, named_sheet: NAMED_SHEET) -> Worksheet:
        """
        Получение объекта Worksheet по имени листа.

        :param named_sheet: Имя листа.
        :return: Объект Worksheet.
        """
        spr_sheet = self.__client.open(NAMED_TABLE)
        return spr_sheet.worksheet(named_sheet)

    def __new_row(self, named_sheet: NAMED_SHEET, values: list) -> None:
        """
        Добавление новой строки в лист.

        :param named_sheet: Имя листа.
        :param values: Список значений для добавления.
        """
        worksheet = self.__get_worksheet(named_sheet)
        data = worksheet.append_row(values)
        logger.info(data)

    @staticmethod
    def __get_values(obj: TypeObjectDB, named_sheet: NAMED_SHEET) -> list | None:
        from internal.entities.database import User
        values = None
        logger.info(type(obj))
        match named_sheet:
            case "users":
                if isinstance(obj, User):
                    values = [
                        obj.id,
                        obj.city,
                        obj.full_name,
                        obj.age,
                        obj.position,
                        obj.ai_level,
                        datetime.datetime.now(MOSCOW_TZ).strftime("%Y-%m-%d %H:%M:%S"),
                    ]
        logger.info(values)
        return values

    @staticmethod
    def __get_index_in_table(worksheet: Worksheet, value) -> int:
        index = worksheet.find(str(value), in_column=1)
        return index.row

    def __update_row(self, named_sheet: NAMED_SHEET, values: list) -> bool:
        """
        Обновление строки в листе.

        :param named_sheet: Имя листа.
        :param values: Список значений для обновления.
        """
        worksheet = self.__get_worksheet(named_sheet)
        index = self.__get_index_in_table(worksheet, values[0])
        cell_list = worksheet.range(f"A{index}:{INDEXES_COLUMNS[len(values)]}{index}")

        for ind, cell in enumerate(cell_list):
            cell.value = values[ind]
        try:
            worksheet.update_cells(cell_list)
            return True
        except Exception as e:
            logger.error(e)
            return False

    async def append(self, obj: TypeObjectDB, named_sheet: NAMED_SHEET) -> bool:
        """
        Добавление объекта в лист.

        :param obj: Объект для добавления.
        :param named_sheet: Имя листа.
        :return: True, если добавление прошло успешно, False в противном случае.
        """
        values = self.__get_values(obj, named_sheet)
        if values is None:
            logger.error(f"Object {type(obj)} does not match the name of the table.")
            return False
        try:
            self.__new_row(named_sheet, values)
            return True
        except Exception as e:
            logger.error(e)
            return False

    async def update(self, obj: TypeObjectDB, named_sheet: NAMED_SHEET) -> bool:
        """
        Обновление объекта в листе.

        :param obj: Объект для обновления.
        :param named_sheet: Имя листа.
        :return: True, если обновление прошло успешно, False в противном случае.
        """
        values = self.__get_values(obj, named_sheet)
        if values is None:
            logger.error(f"Object {type(obj)} does not match the name of the table.")
            return False
        # status = True
        status = self.__update_row(named_sheet, values)
        return status

    async def get_all_table_users(self) -> Participants:
        data = self.__get_worksheet("users")
        values = data.get_all_records()
        participants = Participants.model_validate(values)

        return participants


GoggleClient = Client(SERVICE_ACCOUNT_FILE, SCOPES)

__all__ = (GoggleClient,)
