from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton
import asyncio
from aiogram import Bot, Dispatcher, F
from aiogram.filters import CommandStart, Command
from aiogram.types import Message, FSInputFile, CallbackQuery
import random
from gtts import gTTS
import os
from dotenv import load_dotenv

# Загрузка переменных окружения из файла .env
load_dotenv()
API_TOKEN = os.getenv('TELEGRAM_API_TOKEN')

bot = Bot(token=API_TOKEN)
dp = Dispatcher()

main_keyboard = ReplyKeyboardMarkup(keyboard=[
   [KeyboardButton(text="Тестовая кнопка 1")],
   [KeyboardButton(text="Тестовая кнопка 2"), KeyboardButton(text="Тестовая кнопка 3")]
], resize_keyboard=True)

@dp.message(CommandStart())
async def start(message: Message):
   await message.answer(f'Приветики, {message.from_user.first_name}', reply_markup=main_keyboard)

async def main():
    await dp.start_polling(bot)

if __name__ == '__main__':
    asyncio.run(main())
