from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

def get_city_keyboard():
    """Клавиатура с популярными городами"""
    buttons = [
        [KeyboardButton(text=city) for city in ["Москва", "Санкт-Петербург"]],
        [KeyboardButton(text=city) for city in ["Новосибирск", "Екатеринбург"]],
        [KeyboardButton(text="Одесса")]
    ]
    return ReplyKeyboardMarkup(
        keyboard=buttons,
        resize_keyboard=True,
        one_time_keyboard=True
    )