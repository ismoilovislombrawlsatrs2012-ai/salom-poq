from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

# Simple inline keyboard with common Uzbek cities. Callback data is the city name used by handlers.
inline_murkup = InlineKeyboardMarkup(row_width=3)
buttons = [
    InlineKeyboardButton("Tashkent", callback_data="Tashkent"),
    InlineKeyboardButton("Samarkand", callback_data="Samarkand"),
    InlineKeyboardButton("Bukhara", callback_data="Bukhara"),
    InlineKeyboardButton("Namangan", callback_data="Namangan"),
    InlineKeyboardButton("Andijan", callback_data="Andijan"),
    InlineKeyboardButton("Fergana", callback_data="Fergana"),
    InlineKeyboardButton("Nukus", callback_data="Nukus"),
    InlineKeyboardButton("Urgench", callback_data="Urgench"),
    InlineKeyboardButton("Karshi", callback_data="Karshi"),
]
inline_murkup.add(*buttons)
