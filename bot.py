import logging
import os
import requests
from aiogram import Bot, Dispatcher, types, F
from aiogram.filters import Command
from aiogram.types import Message
from dotenv import load_dotenv
from keyboards import get_city_keyboard

# Загрузка переменных окружения
load_dotenv()

# Настройка логгера
logging.basicConfig(level=logging.INFO)

# Инициализация бота
bot = Bot(token=os.getenv("BOT_TOKEN"))
dp = Dispatcher()

# Константы
WEATHER_URL = "https://api.openweathermap.org/data/2.5/weather"
DEFAULT_CITIES = ["Москва", "Санкт-Петербург", "Новосибирск", "Екатеринбург", "Одесса"]


def get_weather(city: str) -> str:
    """Получение данных о погоде через API"""
    params = {
        'q': city,
        'appid': os.getenv("OWM_API_KEY"),
        'units': 'metric',
        'lang': 'ru'
    }

    try:
        response = requests.get(WEATHER_URL, params=params)
        data = response.json()

        if response.status_code != 200:
            return f"Ошибка: {data.get('message', 'Unknown error')}"

        return format_weather(data)

    except Exception as e:
        logging.error(f"Weather API error: {e}")
        return "⚠️ Ошибка получения данных. Попробуйте позже."


def format_weather(data: dict) -> str:
    """Форматирование данных о погоде"""
    city = data['name']
    temp = data['main']['temp']
    feels_like = data['main']['feels_like']
    humidity = data['main']['humidity']
    wind = data['wind']['speed']
    description = data['weather'][0]['description'].capitalize()
    icon = get_weather_icon(data['weather'][0]['icon'])

    return (
        f"{icon} <b>Погода в {city}</b>\n\n"
        f"🌡 {temp}°C (ощущается как {feels_like}°C)\n"
        f"📝 {description}\n"
        f"💧 Влажность: {humidity}%\n"
        f"🌬 Ветер: {wind} м/с"
    )


def get_weather_icon(code: str) -> str:
    """Получение иконки погоды по коду"""
    icons = {
        '01': '☀️',  # ясно
        '02': '⛅',  # малооблачно
        '03': '☁️',  # облачно
        '04': '☁️',  # пасмурно
        '09': '🌧️',  # дождь
        '10': '🌦️',  # дождь с солнцем
        '11': '⛈️',  # гроза
        '13': '❄️',  # снег
        '50': '🌫️'  # туман
    }
    return icons.get(code[:2], '🌈')


# Обработчики сообщений
@dp.message(Command('start'))
async def start_handler(message: Message):
    await message.answer(
        "🌤️ Привет! Я бот-метеоролог.\n"
        "Отправь мне название города или выбери из списка:",
        reply_markup=get_city_keyboard()
    )

@dp.message(Command('help'))
async def help_handler(message: Message):
    await message.answer(
        "Этот бот умеет выполнять команды:"
        "\n/start"  "- Запуск бота"
        "\n/help"  "- Помощь"
        "\n/cities"  "- Выбор города",
        reply_markup = get_city_keyboard()

    )

@dp.message(Command("cities"))
async def cities_handler(message: Message):
    await message.answer(
        "Выберите город:",
        reply_markup=get_city_keyboard()
    )


@dp.message(F.text)
async def weather_handler(message: Message):
    city = message.text.strip()
    weather = get_weather(city)
    await message.answer(weather, parse_mode="HTML")




# Запуск бота
if __name__ == "__main__":
    logging.info("Бот запущен")
    dp.run_polling(bot)