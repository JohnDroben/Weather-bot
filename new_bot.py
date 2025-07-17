import logging
import os
import random
import asyncio

from deep_translator import GoogleTranslator
from dotenv import load_dotenv
from aiogram import Bot, Dispatcher, F
from aiogram.filters import Command
from aiogram.types import Message, FSInputFile
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from gtts import gTTS


load_dotenv()
logging.basicConfig(level=logging.INFO)

bot = Bot(token=os.getenv("BOT_TOKEN"))
dp = Dispatcher()

# Определение состояний для FSM
# Определение состояний для FSM
class TranslationStates(StatesGroup):
    waiting_for_text = State()



@dp.message(Command('start'))
async def start_handler(message: Message):
    await message.answer(
        f'Приветики  {message.from_user.first_name}, я бот, который умеет:\n'
        "\n/help"  "- Помощь"
        "\n/photo"  "- Фото"
        "\n/audio"  "- Аудио"
        "\n/video"  "- Видео"
        "\n/document"  "- Документ"
        "\n/location"  "- Геолокация"
        "\n/game"  "- Кости"
        "\n/contact"  "- Контакт"
        "\n/training"  "- Тренировка"
        "\n/translate"  "- Перевод"

    )
@dp.message(Command('help'))
async def help_handler(message: Message):
    await message.answer(
        "Вот что я умею:\n"
        "\n/start"  "- Запуск бота"
        "\n/help"  "- Помощь"
        "\n/photo"  "- Фото"
        "\n/audio"  "- Аудио"
        "\n/video"  "- Видео"
        "\n/document"  "- Документ"
        "\n/location"  "- Геолокация"
        "\n/game"  "- Кости"
        "\n/contact"  "- Контакт"
        "\n/training"  "- Тренировка"
        "\n/translate"  "- Перевод"
    )

@dp.message(Command('photo'))
async def photo_handler(message: Message):
    List = ["https://www.sample-videos.com/img/Sample-jpg-image-50kb.jpg",
            "https://www.sample-videos.com/img/Sample-jpg-image-100kb.jpg"

    ]
    rend_photo = random.choice(List)
    await message.answer_photo(photo=rend_photo, caption="Это лучшее фото")

@dp.message(Command('audio'))
async def audio_handler(message: Message):
    await message.answer_audio(
        audio="https://www.soundhelix.com/examples/mp3/SoundHelix-Song-1.mp3"
    )

@dp.message(Command('video'))
async def video_handler(message: Message):
    await bot.send_chat_action(message.chat.id, action="upload_video")
    video = FSInputFile ("bunny-review-kitty-review.mp4")
    await bot.send_video(message.chat.id, video=video)

@dp.message(Command('document'))
async def document_handler(message: Message):
    await message.answer_document
    document = "https://www.w3.org/WAI/ER/tests/xhtml/testfiles/resources/pdf/dummy.pdf"
    await message.answer_document(document=document)

@dp.message(Command('location'))
async def location_handler(message: Message):
    await message.answer_location(
        latitude=59.9386,
        longitude=30.3141
    )
@dp.message(Command('game'))
async def dice_handler(message: Message):
    await message.answer_dice()

@dp.message(Command('contact')) # Контакт
async def contact_handler(message: Message):
    await message.answer_contact(
        phone_number="+1234567890",
        first_name="John",
        last_name="Doe"
    )
@dp.message(Command('training'))
async def training_handler(message: Message):
    training_list = ["Тренировка на сегодня:\n"
                    "Занятие 1:Основной блок (20 мин): 3 круга. Отдых между кругами 60 сек. Отдых между упражнениями 15 сек. "
                                  "Приседания (воздушные): 12-15 повторений. Отжимания (с колен или от стены, если сложно): 8-12 повторений."
                                  "Планка: 20-30 секунд. Выпады на месте (попеременно): 10-12 на каждую ногу. Скручивания: 15-20 повторений.\n",
                    
                    "Занятие 2: Болгарские сплит-приседы (задняя нога на диване/стуле): 10-12 на каждую ногу. "
                                "Подъемы на носки: 20-25 повторений (можно с книгой в руках). "
                                "Кардио-интервал: Прыжки (Jumping Jacks) - 45 секунд ВСЕХ СИЛ, отдых 30 сек. Повторить 3 раза. "
                                "Заминка (5 мин): Растяжка ног и ягодиц\n",
                                                              
                    "Занятие 3: Статичные позы йоги (удержание 30-60 сек каждая): Поза ребенка. Поза кошки-коровы (динамично, 10 раз)."
                                "Собака мордой вниз. Поза голубя (на каждую ногу). Наклон вперед сидя (Пашчимоттанасана). "
                                "Скручивание сидя (Ардха Матсиендрасана). Поза моста (схожа с ягодичным мостиком, удержание). Поза бабочки. "
                                "Заминка (3 мин): Шавасана (поза мертвеца) - полное расслабление, фокус на дыхании.\n",
                                                              
                    "Занятие 4. Верх тела и Пресс: Отжимания: 8-12 повторений (любой вариант: от стены, с колен, классика). "
                                "Обратные отжимания от стула/дивана (на трицепс): 10-15 повторений."
                                "Супермен: 12-15 повторений (лежа на животе, поднимаем руки и ноги)." 
                                "Велосипед (на пресс): 20 повторений (10 вращений в каждую сторону).Планка на предплечьях: 30-45 секунд.\n",
                                                              
                    "Занятие 5. Силовые упражнения: Подъемы на носки: 20-25 повторений (можно с книгой в руках). "
                                "Кардио-интервал: Прыжки (Jumping Jacks) - 45 секунд ВСЕХ СИЛ, отдых 30 сек. Повторить 3 раза. "
                                "Заминка (5 мин): Растяжка ног и ягодиц\n",


    ]
    rand_tr = random.choice(training_list)
    await message.answer(f'Тренировка на сегодня:\n {rand_tr}')

    tts = gTTS(text=rand_tr, lang='ru')
    tts.save("training.mp3")
    audio = FSInputFile(path='training.mp3')
    await bot.send_audio(message.chat.id, audio)
    os.remove("training.mp3")


@dp.message(Command('translate'))
async def translate_command_handler(message: Message, state: FSMContext):
    await message.answer("Введите текст для перевода:")
    await state.set_state(TranslationStates.waiting_for_text)


@dp.message(TranslationStates.waiting_for_text)
async def process_translation(message: Message, state: FSMContext):
    try:
        # Асинхронный перевод с deep_translator
        def sync_translate():
            return GoogleTranslator(source='auto', target='en').translate(message.text)

        translation = await asyncio.to_thread(sync_translate)
        await message.answer(f"Перевод: {translation}")
    except Exception as e:
        logging.error(f"Translation error: {e}")
        await message.answer("Произошла ошибка при переводе. Попробуйте позже.")
    finally:
        await state.clear()


@dp.message(F.text)  # ЭХО-бот: Обработка текстовых сообщений
async def echo_handler(message: Message):
    await message.answer(message.text)



if __name__ == "__main__":
    dp.run_polling(bot)