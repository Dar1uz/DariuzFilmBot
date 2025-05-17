from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

main = ReplyKeyboardMarkup(keyboard=[
    [KeyboardButton(text="🔍 Поиск")],
    [KeyboardButton(text="🎲 Рандом")],
    [KeyboardButton(text="⚙️ Предпочтения")],
])

random = ReplyKeyboardMarkup(keyboard=[
    [KeyboardButton(text="🎲 Рандом")],
    [KeyboardButton(text="🏠 На главную")],
])

film = ReplyKeyboardMarkup(keyboard=[
    [KeyboardButton(text="🔍 Поиск")],
    [KeyboardButton(text="🏠 На главную")],
])

main_settings = ReplyKeyboardMarkup(keyboard=[
    [KeyboardButton(text="Тип"), KeyboardButton(text="Жанр"), KeyboardButton(text="Год")],
    [KeyboardButton(text="Страна"), KeyboardButton(text="Длительность")],
    [KeyboardButton(text="💾 Сохранить")]
])

settings_list = ReplyKeyboardMarkup(keyboard=[
    [KeyboardButton(text="📋 Вывести список")],
    [KeyboardButton(text="↩️ Назад")],
    [KeyboardButton(text="💾 Сохранить")],
])

settings = ReplyKeyboardMarkup(keyboard=[
    [KeyboardButton(text="↩️ Назад")],
    [KeyboardButton(text="💾 Сохранить")],
])