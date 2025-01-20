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
import aiohttp

# Загрузка переменных окружения из файла .env
load_dotenv()

API_TOKEN = os.getenv('TELEGRAM_API_TOKEN')
API_LINK = os.getenv('API_LINK')

# Проверка, что переменные окружения корректно загружены
if not API_TOKEN or not API_LINK:
    raise ValueError("API_TOKEN и API_LINK должны быть заданы в файле .env")

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
        keyboard.add(InlineKeyboardButton(text=key, callback_data=key))
    return keyboard.adjust(2).as_markup()

@dp.message(CommandStart())
async def start(message: Message):
    await message.answer(f'Здарова! {message.from_user.first_name}', reply_markup=await test_keyboard())

@dp.callback_query(lambda c: c.data in urls.keys())
async def process_callback_button(callback_query: CallbackQuery):
    selected_url = urls[callback_query.data]
    keyboard = InlineKeyboardBuilder()
    keyboard.add(InlineKeyboardButton(text="Cancel", callback_data="cancel"))
    keyboard.add(InlineKeyboardButton(text="OK", callback_data="ok"))
    keyboard.add(InlineKeyboardButton(text="Go to API", callback_data="go_to_api"))
    await callback_query.message.answer(f'Открыть эту ссылку: {selected_url}?', reply_markup=keyboard.as_markup())

@dp.callback_query(lambda c: c.data == 'cancel')
async def process_callback_cancel(callback_query: CallbackQuery):
    await callback_query.message.answer('Вы нажали Cancel')

@dp.callback_query(lambda c: c.data == 'ok')
async def process_callback_ok(callback_query: CallbackQuery):
    await callback_query.message.answer('Вы нажали OK')

@dp.callback_query(lambda c: c.data == 'go_to_api')
async def process_callback_go_to_api(callback_query: CallbackQuery):
    async with aiohttp.ClientSession() as session:
        async with session.get(API_LINK, headers={"Authorization": f"Bearer {API_TOKEN}"}) as response:
            if response.status == 200:
                await callback_query.message.answer('Вызов API выполнен успешно')
            else:
                await callback_query.message.answer('Ошибка при вызове API')

async def main():
    await dp.start_polling(bot)

if __name__ == '__main__':
    asyncio.run(main())
