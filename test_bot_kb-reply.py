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



main_keyboard = ReplyKeyboardMarkup(keyboard=[
   [KeyboardButton(text="Тестовая кнопка 1")],
   [KeyboardButton(text="Тестовая кнопка 2"), KeyboardButton(text="Тестовая кнопка 3")]
], resize_keyboard=True)
@dp.message(CommandStart())
async def start(message: Message):
    await message.answer(f'Привет! {message.from_user.first_name}', reply_markup=main_keyboard)

@dp.message(F.text == "Тестовая кнопка 1")
async def test_button1(message: Message):
   await message.answer('Обработка нажатия на Тестовую кнопку 1')
@dp.message(F.text == "Тестовая кнопка 2")
async def test_button2(message: Message):
   await message.answer('Обработка нажатия на Тестовую кнопку 2')

async def main():
    await dp.start_polling(bot)


if __name__ == '__main__':
    asyncio.run(main())

""" 
test = ["кнопка 1", "кнопка 2", "кнопка 3", "кнопка 4"]
async def test_keyboard():
    keyboard = InlineKeyboardBuilder()
    for key in test:
        keyboard.add(InlineKeyboardButton(text=key, callback_data=key))
    return keyboard.adjust(2).as_markup()
@dp.message(CommandStart())
async def start(message: Message):
    await message.answer(f'Приветики, {message.from_user.first_name}', reply_markup=await test_keyboard())



inline_keyboard_test = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="Видео", url='https://www.youtube.com/watch?v=HfaIcB4Ogxk')],])
    @dp.message(CommandStart())
    async def start(message: Message):
        await message.answer(f'Приветики, {message.from_user.first_name}', reply_markup=inline_keyboard_test)


"""
