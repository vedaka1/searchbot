from aiogram import types

from domain.common.enums import Categories


class Keyboards:
    categories = Categories

    def update_category_keyboard(self):
        buttons = [
            [
                types.InlineKeyboardButton(
                    text=search_type.value, callback_data=f"update_{search_type.value}"
                )
            ]
            for search_type in self.categories
        ]
        return buttons

    def search_category_keyboard(self):
        buttons = [
            [
                types.InlineKeyboardButton(
                    text=search_type.value, callback_data=f"search_{search_type.value}"
                )
            ]
            for search_type in self.categories
        ]
        return buttons

    def request_access_keyboard(self, from_user: int):
        buttons = [
            [
                types.InlineKeyboardButton(
                    text="Принять", callback_data=f"requestAccess_accept_{from_user}"
                )
            ],
            [
                types.InlineKeyboardButton(
                    text="Отказать", callback_data=f"requestAccess_reject_{from_user}"
                )
            ],
        ]
        return buttons


kb = Keyboards()
