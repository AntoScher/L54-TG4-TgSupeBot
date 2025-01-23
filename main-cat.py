import asyncio
import requests
from aiogram import Bot, Dispatcher, types
from aiogram.filters import CommandStart
from aiogram.types import Message, CallbackQuery, InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder
from googleapiclient.discovery import build
import os
from dotenv import load_dotenv
import logging
from foto_main import search_photos  # Импортируем функцию из второго файла

# Загрузка переменных окружения из файла .env
load_dotenv()
API_TOKEN = os.getenv('TELEGRAM_API_TOKEN')
API_KEY_NEWS = os.getenv('API_KEY_NEWS')
YOUTUBE_API_KEY = os.getenv('YOUTUBE_API_KEY')

# Проверка, что переменные окружения корректно загружены
if not API_TOKEN or not API_KEY_NEWS or not YOUTUBE_API_KEY:
    raise ValueError("API_TOKEN и API_KEY_NEWS должны быть заданы в файле .env")
# Настройка логирования
logging.basicConfig(level=logging.INFO)

bot = Bot(token=API_TOKEN)
dp = Dispatcher()

urls = {
    "кнопка 1": "https://dzen.ru/news/?issue_tld=ru",
    "кнопка 2": "https://www.youtube.com/news",
    "кнопка 3": "Искать фото на Unsplash",
}


async def test_keyboard():
    keyboard = InlineKeyboardBuilder()
    for key in urls.keys():
        keyboard.add(InlineKeyboardButton(text=key, callback_data=key))
    return keyboard.adjust(3).as_markup()


@dp.message(CommandStart())
async def start(message: Message):
    await message.answer(f'Привет! {message.from_user.first_name}', reply_markup=await test_keyboard())


@dp.callback_query(lambda c: c.data in urls.keys())
async def process_callback_button(callback_query: CallbackQuery):
    selected_url = urls[callback_query.data]

    if callback_query.data == "кнопка 3":
        await callback_query.message.answer("Введите запрос для поиска фото на Unsplash:")
        return

    keyboard = InlineKeyboardBuilder()
    keyboard.add(InlineKeyboardButton(text="Go to hot news", callback_data="get_news"))
    await callback_query.message.answer(f"Открыть эту ссылку: {selected_url}?", reply_markup=keyboard.as_markup())


@dp.message(lambda message: message.text and message.chat.type == 'private')
async def process_text_query(message: Message):
    query = message.text.strip()

    # Проверяем, если это запрос на поиск фото
    if query and query.startswith("http"):  # Предположим, что это условие для поиска фото
        await search_photos(message)  # Вызов функции поиска фото
        return

    # Остальная часть вашего кода...


# Другие части вашего кода остаются без изменений...

async def main():
    await dp.start_polling(bot)


if __name__ == '__main__':
    asyncio.run(main())