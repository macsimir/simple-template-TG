from aiogram import types

def admin_panel_keyboard():
    buttons = [
        [types.InlineKeyboardButton(text="Пользователи", callback_data="show_users")]
    ]
    keyboard = types.InlineKeyboardMarkup(inline_keyboard=buttons)
    return keyboard