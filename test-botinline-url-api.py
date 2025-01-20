from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton
import asyncio
from aiogram import Bot, Dispatcher, F
from aiogram.filters import CommandStart, Command
from aiogram.types import Message, FSInputFile, CallbackQuery
import random
from gtts import gTTS
import os
from dotenv import load_dotenv
from aiogram.utils.keyboard import ReplyKeyboardBuilder, InlineKeyboardBuilder

# Загрузка переменных окружения из файла .env
load_dotenv()
API_TOKEN = os.getenv('TELEGRAM_API_TOKEN')

bot = Bot(token=API_TOKEN)
dp = Dispatcher()

urls = {
    "кнопка 1": "https://example.com/link1",
    "кнопка 2": "https://example.com/link2",
    "кнопка 3": "https://example.com/link3",
    "кнопка 4": "https://example.com/link4"
}

async def test_keyboard():
    keyboard = InlineKeyboardBuilder()
    for key, url in urls.items():
        keyboard.add(InlineKeyboardButton(text=key, url=url))
    return keyboard.adjust(2).as_markup()

@dp.message(CommandStart())
async def start(message: Message):
    await message.answer(f'Здарова! {message.from_user.first_name}', reply_markup=await test_keyboard())

async def main():
    await dp.start_polling(bot)

if __name__ == '__main__':
    asyncio.run(main())
