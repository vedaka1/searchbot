from aiogram import types

category_keyboard = [
    [
        types.InlineKeyboardButton(
            text=search_type, callback_data=f"search_{search_type}"
        )
    ]
    for search_type in ["Сотрудник", "Документ"]
]


def request_access_keyboard(from_user: int):
    return [
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
