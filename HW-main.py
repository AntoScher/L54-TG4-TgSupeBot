from aiogram import Bot, Dispatcher, types
from aiogram.filters import Command
from aiogram.types import Message, ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton
import asyncio
import os
from dotenv import load_dotenv

# Загрузка переменных окружения из файла .env
load_dotenv()
API_TOKEN = os.getenv('TELEGRAM_API_TOKEN')

bot = Bot(token=API_TOKEN)
dp = Dispatcher()

# Главное меню с reply-кнопками
main_menu = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text='Привет')],
        [KeyboardButton(text='Пока')],
        [KeyboardButton(text='Меню')],
        [KeyboardButton(text='Ещё')]
    ],
    resize_keyboard=True
)

# Инлайн-кнопки для "Меню"
menu_inline = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text='Новости', callback_data='news')],
    [InlineKeyboardButton(text='Музыка', callback_data='music')],
    [InlineKeyboardButton(text='Видео', callback_data='video')]
])

# Инлайн-кнопки для "Ещё"
extra_inline = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text='Порисуем?', callback_data='draw')],
    [InlineKeyboardButton(text='Поболтаем?', callback_data='chat')]
])

@dp.message(Command('start'))
async def start(message: Message):
    await message.answer('Выберите опцию:', reply_markup=main_menu)

@dp.message(lambda message: message.text == 'Привет')
async def greet(message: Message):
    await message.answer(f'Привет, {message.from_user.first_name}!')

@dp.message(lambda message: message.text == 'Пока')
async def farewell(message: Message):
    await message.answer(f'До свидания, {message.from_user.first_name}!')

@dp.message(lambda message: message.text == 'Меню')
async def menu(message: Message):
    await message.answer('Выберите опцию:', reply_markup=menu_inline)

@dp.message(lambda message: message.text == 'Ещё')
async def extra(message: Message):
    await message.answer('Выберите опцию:', reply_markup=extra_inline)

@dp.callback_query(lambda c: c.data == 'news')
async def news(callback_query: types.CallbackQuery):
    await callback_query.message.answer(f'Вот ваши новости! Открыть эту ссылку: https://www.youtube.com/news', reply_markup=InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text='Cancel', callback_data='cancel')],
            [InlineKeyboardButton(text='Open', url='https://www.youtube.com/news')]
        ]))

@dp.callback_query(lambda c: c.data == 'music')
async def music(callback_query: types.CallbackQuery):
    await callback_query.message.answer(f'Вот ваша музыка! Открыть эту ссылку: https://www.youtube.com/music', reply_markup=InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text='Cancel', callback_data='cancel')],
            [InlineKeyboardButton(text='Open', url='https://www.youtube.com/music')]
        ]))

@dp.callback_query(lambda c: c.data == 'video')
async def video(callback_query: types.CallbackQuery):
    await callback_query.message.answer(f'Вот ваше видео! Открыть эту ссылку: https://www.youtube.com/video', reply_markup=InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text='Cancel', callback_data='cancel')],
            [InlineKeyboardButton(text='Open', url='https://www.youtube.com/video')]
        ]))

@dp.callback_query(lambda c: c.data == 'draw')
async def draw(callback_query: types.CallbackQuery):
    await callback_query.message.answer('Давайте порисуем!')

@dp.callback_query(lambda c: c.data == 'chat')
async def chat(callback_query: types.CallbackQuery):
    await callback_query.message.answer('Давайте поболтаем!')

@dp.callback_query(lambda c: c.data == 'cancel')
async def process_callback_cancel(callback_query: types.CallbackQuery):
    await callback_query.message.answer('Вы отменили действие')

async def main():
    await dp.start_polling(bot)

if __name__ == '__main__':
    asyncio.run(main())
