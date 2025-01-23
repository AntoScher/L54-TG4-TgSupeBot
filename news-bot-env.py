import asyncio
import requests
from aiogram import Bot, Dispatcher, types
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.filters import CommandStart, Command
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram import Router
import os
from dotenv import load_dotenv

# Загрузка переменных окружения из файла .env
load_dotenv()

API_TOKEN = os.getenv('TELEGRAM_API_TOKEN')
API_KEY_NEWS = os.getenv('API_KEY_NEWS')
# Проверка, что переменные окружения коррAPI_KEY_NEWSектно загружены
if not API_TOKEN or not API_KEY_NEWS:
    raise ValueError("API_TOKEN и API_KEY_NEWS должны быть заданы в файле .env")

bot = Bot(token=API_TOKEN)
storage = MemoryStorage()
dp = Dispatcher(storage=storage)
router = Router()

def get_news():
    url = 'https://newsapi.org/v2/top-headlines?'
    params = {
        'country': 'us',
        'apiKey':API_KEY_NEWS,
        'category': 'general',  # Попробуйте добавить категорию
        'pageSize': 5  # Ограничим количество возвращаемых новостей
    }
    response = requests.get(url, params=params)
    print(f"Response status code: {response.status_code}")  # Отладка статуса ответа
    if response.status_code != 200:
        print(f"Error: {response.text}")  # Отладка текста ошибки
        return ["Не удалось получить новости."]

    data = response.json()
    print(f"Response data: {data}")  # Отладка данных ответа
    news = []
    for article in data['articles']:
        news.append(f"{article['title']}\n{article['url']}")
    print(f"Collected news: {news}")  # Отладка собранных новостей
    return news


# Обработчик нажатия на inline кнопку
@router.callback_query(lambda c: c.data == 'get_news')
async def process_callback_button(callback_query: types.CallbackQuery):
    await callback_query.answer()
    news = get_news()
    for item in news:
        print(f"Sending news item: {item}")  # Отладка отправляемого сообщения
        await bot.send_message(callback_query.from_user.id, item)


# Обработчик команды /start
@router.message(CommandStart())
async def send_welcome(message: types.Message):
    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="Получить новости", callback_data='get_news')]
    ])
    await message.answer('Привет! Нажми на кнопку, чтобы получить новости', reply_markup=keyboard)


async def main():
    dp.include_router(router)
    await dp.start_polling(bot)


if __name__ == '__main__':
    asyncio.run(main())
