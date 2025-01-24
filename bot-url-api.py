import asyncio
import requests
from aiogram import Bot, Dispatcher, types
from aiogram.filters import CommandStart
from aiogram.types import Message, CallbackQuery, InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder
from googleapiclient.discovery import build
import os
from dotenv import load_dotenv
import logging

# Загрузка переменных окружения из файла .env
load_dotenv()
API_TOKEN = os.getenv('TELEGRAM_API_TOKEN')
API_KEY_NEWS = os.getenv('API_KEY_NEWS')
YOUTUBE_API_KEY = os.getenv('YOUTUBE_API_KEY')

# Проверка, что переменные окружения корректно загружены
if not API_TOKEN or not API_KEY_NEWS or not YOUTUBE_API_KEY:
    raise ValueError("API_TOKEN, API_KEY_NEWS и YOUTUBE_API_KEY должны быть заданы в файле .env")

# Настройка логирования
logging.basicConfig(level=logging.INFO)

bot = Bot(token=API_TOKEN)
dp = Dispatcher()

urls = {
    "новости": "https://dzen.ru/news/?issue_tld=ru",
    "видео": "https://www.youtube.com/news",
    "фото": "https://example.com/link3",
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
    if callback_query.data == "кнопка 2":
        keyboard.add(InlineKeyboardButton(text="Поиск ссылок YouTube", callback_data="search_youtube"))
    else:
        keyboard.add(InlineKeyboardButton(text="Go to hot news", callback_data="get_news"))
    await callback_query.message.answer(f"Открыть эту ссылку: {selected_url}?", reply_markup=keyboard.as_markup())

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

# Инициализация YouTube API клиента
youtube = build('youtube', 'v3', developerKey=YOUTUBE_API_KEY)

# Обработчик нажатия на инлайн-кнопку "Поиск ссылок YouTube"
@dp.callback_query(lambda callback_query: callback_query.data == "search_youtube")
async def search_youtube(callback_query: CallbackQuery):
    await callback_query.message.answer("Введите текстовый запрос для поиска YouTube видео:")

# Обработка текстового запроса после нажатия инлайн-кнопки
@dp.message(lambda message: message.text and message.chat.type == 'private')
async def process_text_query(message: Message):
    query = message.text.strip()
    if not query:
        await message.reply("Пожалуйста, предоставьте текстовое описание для поиска.")
        logging.info("Запрос пустой.")
        return
    logging.info(f"Поисковый запрос: {query}")
    try:
        search_response = youtube.search().list(
            q=query,
            part="snippet",
            maxResults=1
        ).execute()
        logging.info(f"Ответ API: {search_response}")
        if 'items' in search_response and search_response['items']:
            video_id = search_response['items'][0]['id']['videoId']
            video_url = f"https://www.youtube.com/watch?v={video_id}"
            video_title = search_response['items'][0]['snippet']['title']
            logging.info(f"Видео найдено: {video_title}, {video_url}")
            await message.reply(f"**Название:** {video_title}\n**Ссылка:** {video_url}")
        else:
            logging.info("Видео по вашему запросу не найдено.")
            await message.reply("Видео по вашему запросу не найдено.")
    except Exception as e:
        logging.error(f"Произошла ошибка при выполнении поиска: {e}")
        await message.reply(f"Произошла ошибка при выполнении поиска. Ошибка: {str(e)}")

async def main():
    dp.message.register(start, CommandStart())
    dp.callback_query.register(search_youtube, lambda callback_query: callback_query.data == "search_youtube")
    dp.callback_query.register(process_get_news, lambda callback_query: callback_query.data == "get_news")
    dp.message.register(process_text_query, lambda message: message.text and message.chat.type == 'private')
    await dp.start_polling(bot)

if __name__ == '__main__':
    asyncio.run(main())
