from aiogram import types

category_keyboard = [
    [
        types.InlineKeyboardButton(
            text=search_type, callback_data=f"search_{search_type}"
        )
    ]
    for search_type in ["Сотрудник", "Документ"]
]
