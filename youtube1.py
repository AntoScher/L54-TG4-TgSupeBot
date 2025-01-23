import os
from dotenv import load_dotenv
import logging
import asyncio
from aiogram import Bot, Dispatcher, types
from aiogram.filters import CommandStart, Command
from aiogram.types import Message
from googleapiclient.discovery import build

# Загрузка переменных окружения из файла .env
load_dotenv()

API_TOKEN = os.getenv('TELEGRAM_API_TOKEN')
YOUTUBE_API_KEY = os.getenv('YOUTUBE_API_KEY')

# Настройка логирования
logging.basicConfig(level=logging.INFO)

# Инициализация бота и диспетчера
bot = Bot(token=API_TOKEN)
dp = Dispatcher()

# Инициализация YouTube API клиента
youtube = build('youtube', 'v3', developerKey=YOUTUBE_API_KEY)

# Пример хендлера с использованием CommandStart
@dp.message(CommandStart())
async def start(message: Message):
    await message.answer("Привет! Отправьте мне текстовый запрос и получите ссылку на YouTube-видео (/look ...запрос...)")

# Прописываем хендлер для команды /look
@dp.message(Command(commands=["look"]))
async def look_command(message: Message):
    query = message.text[len("/look "):].strip()
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
    dp.message.register(look_command, Command(commands=["look"]))

    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
