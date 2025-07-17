import logging
import os
import asyncio
import sqlite3
import aiohttp

from dotenv import load_dotenv
from aiogram import Bot, Dispatcher
from aiogram.filters import Command
from aiogram.types import Message
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup

load_dotenv()
logging.basicConfig(level=logging.INFO)

bot = Bot(token=os.getenv("BOT_TOKEN"))
dp = Dispatcher()


class Form(StatesGroup):
    name = State()
    age = State()
    grade = State()
    city = State()


def init_db():
    conn = sqlite3.connect('school_data.db')
    cur = conn.cursor()
    cur.execute('''CREATE TABLE IF NOT EXISTS students (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    name TEXT NOT NULL,
                    age INTEGER NOT NULL,
                    grade TEXT NOT NULL,
                    city TEXT NOT NULL
                )''')
    conn.commit()
    conn.close()


init_db()


# Функция для получения иконки погоды
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


@dp.message(Command('start'))
async def start_handler(message: Message, state: FSMContext):
    await message.answer("Привет! Как тебя зовут?", reply_markup=None)
    await state.set_state(Form.name)


@dp.message(Form.name)
async def process_name(message: Message, state: FSMContext):
    await state.update_data(name=message.text)
    await message.answer("Сколько тебе лет?")
    await state.set_state(Form.age)


@dp.message(Form.age)
async def process_age(message: Message, state: FSMContext):
    try:
        age = int(message.text)
        if age < 5 or age > 20:
            await message.answer("Пожалуйста, введите реальный возраст (5-20 лет)")
            return
        await state.update_data(age=age)
        await message.answer("Какой у тебя класс?")
        await state.set_state(Form.grade)
    except ValueError:
        await message.answer("Пожалуйста, введите число для возраста")


@dp.message(Form.grade)
async def process_grade(message: Message, state: FSMContext):
    await state.update_data(grade=message.text)
    await message.answer("В каком городе ты живешь?")
    await state.set_state(Form.city)


@dp.message(Form.city)
async def process_city(message: Message, state: FSMContext):
    city = message.text
    await state.update_data(city=city)
    data = await state.get_data()

    # Форматируем ответ
    response = (
        f"✅ Ваши данные сохранены:\n"
        f"👤 Имя: {data['name']}\n"
        f"🎂 Возраст: {data['age']}\n"
        f"🏫 Класс: {data['grade']}\n"
        f"📍 Город: {city}"
    )
    await message.answer(response)

    # Сохраняем в базу данных
    try:
        conn = sqlite3.connect('school_data.db')
        cur = conn.cursor()
        cur.execute('''
            INSERT INTO students (name, age, grade, city) 
            VALUES (?, ?, ?, ?)''',
                    (data['name'], data['age'], data['grade'], city))
        conn.commit()
        conn.close()
    except sqlite3.Error as e:
        logging.error(f"Database error: {e}")
        await message.answer("⚠️ Произошла ошибка при сохранении данных")

    # Получаем погоду
    try:
        async with aiohttp.ClientSession() as session:
            url = f"https://api.openweathermap.org/data/2.5/weather?q={city}&appid={os.getenv('OWM_API_KEY')}&units=metric&lang=ru"
            async with session.get(url) as response:
                if response.status == 200:
                    weather_data = await response.json()
                    temp = weather_data['main']['temp']
                    feels_like = weather_data['main']['feels_like']
                    humidity = weather_data['main']['humidity']
                    wind = weather_data['wind']['speed']
                    description = weather_data['weather'][0]['description'].capitalize()
                    icon = get_weather_icon(weather_data['weather'][0]['icon'])

                    weather_response = (
                        f"{icon} <b>Погода в {city}</b>\n\n"
                        f"🌡 Температура: {temp}°C\n"
                        f"🌡 Ощущается как: {feels_like}°C\n"
                        f"💧 Влажность: {humidity}%\n"
                        f"🌬 Ветер: {wind} м/с\n"
                        f"📝 Описание: {description}"
                    )
                    await message.answer(weather_response)
                else:
                    error_text = await response.text()
                    await message.answer(f"⚠️ Ошибка получения погоды: {response.status} - {error_text}")
    except Exception as e:
        logging.error(f"Weather API error: {e}")
        await message.answer("⚠️ Произошла ошибка при получении данных о погоде")

    await state.clear()


async def main():
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())


