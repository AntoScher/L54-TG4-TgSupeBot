import asyncio
import requests
from aiogram import Bot, Dispatcher, types
from aiogram.filters import CommandStart
from aiogram.types import Message, CallbackQuery, InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder
import os
from dotenv import load_dotenv

# Загрузка переменных окружения из файла .env
load_dotenv()

API_TOKEN = os.getenv('TELEGRAM_API_TOKEN')
API_KEY_NEWS = os.getenv('API_KEY_NEWS')

# Проверка, что переменные окружения корректно загружены
if not API_TOKEN or not API_KEY_NEWS:
    raise ValueError("API_TOKEN и API_KEY_NEWS должны быть заданы в файле .env")

bot = Bot(token=API_TOKEN)
dp = Dispatcher()

urls = {
    "кнопка 1": "https://dzen.ru/news/?issue_tld=ru",
    "кнопка 2": "https://www.youtube.com/news",
    "кнопка 3": "https://example.com/link3",
    #"кнопка 4": "https://example.com/link4"
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
    keyboard = InlineKeyboardBuilder()
    keyboard.add(InlineKeyboardButton(text="Go to hot video", callback_data="get_video"))
    await callback_query.message.answer(f"Открой эту ссылку: {selected_url}", reply_markup=keyboard.as_markup())

def get_news():
    url = 'https://newsapi.org/v2/top-headlines'
    params = {
        'country': 'us',
        'apiKey': API_KEY_NEWS,
        'category': 'general',
        'pageSize': 5
    }
    response = requests.get(url, params=params)
    print(f"Response status code: {response.status_code}")
    if response.status_code != 200:
        print(f"Error: {response.text}")
        return ["Не удалось получить новости."]

    data = response.json()
    news = []
    for article in data.get('articles', []):
        title = article.get('title', 'Без названия')
        link = article.get('url', '')
        news.append(f"{title}\n{link}")
    return news

@dp.callback_query(lambda c: c.data == "get_news")
async def process_get_news(callback_query: CallbackQuery):
    await callback_query.answer()
    news_items = get_news()
    for item in news_items:
        await bot.send_message(callback_query.from_user.id, item)


@dp.callback_query(lambda c: c.data in urls.keys())
async def process_callback_button(callback_query: CallbackQuery):
    selected_url = urls[callback_query.data]
    keyboard = InlineKeyboardBuilder()
    keyboard.add(InlineKeyboardButton(text="Go to hot news", callback_data="get_news"))
    await callback_query.message.answer(f"Открой эту ссылку: {selected_url}", reply_markup=keyboard.as_markup())

def get_news():
    url = 'https://newsapi.org/v2/top-headlines'
    params = {
        'country': 'us',
        'apiKey': API_KEY_NEWS,
        'category': 'general',
        'pageSize': 5
    }
    response = requests.get(url, params=params)
    print(f"Response status code: {response.status_code}")
    if response.status_code != 200:
        print(f"Error: {response.text}")
        return ["Не удалось получить новости."]

    data = response.json()
    news = []
    for article in data.get('articles', []):
        title = article.get('title', 'Без названия')
        link = article.get('url', '')
        news.append(f"{title}\n{link}")
    return news

@dp.callback_query(lambda c: c.data == "get_news")
async def process_get_news(callback_query: CallbackQuery):
    await callback_query.answer()
    news_items = get_news()
    for item in news_items:
        await bot.send_message(callback_query.from_user.id, item)








async def main():
    await dp.start_polling(bot)

if __name__ == '__main__':
    asyncio.run(main())
