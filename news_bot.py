import asyncio
from aiogram import Bot, Dispatcher, executor, types
import requests

# Замените 'YOUR_TOKEN' и 'YOUR_API_KEY' на свои значения
bot = Bot(token='YOUR_TOKEN')
dp = Dispatcher(bot)

def get_news():
    url = 'https://newsapi.org/v2/top-headlines?country=ru&apiKey=YOUR_API_KEY'
    response = requests.get(url)
    data = response.json()
    news = []
    for article in data['articles']:
        news.append(f"{article['title']}\n{article['url']}")
    return news

# Обработчик нажатия на inline кнопку
@dp.callback_query_handler(text='get_news')
async def process_callback_button(callback_query: types.CallbackQuery):
    await callback_query.answer()

    news = get_news()
    for item in news:
        await bot.send_message(callback_query.from_user.id, item)

# Хэндлер для начального сообщения с кнопкой
@dp.message_handler(commands=['start'])
async def send_welcome(message: types.Message):
    markup = types.InlineKeyboardMarkup()
    button = types.InlineKeyboardButton("Получить новости", callback_data='get_news')
    markup.add(button)
    await message.answer('Привет! Нажми на кнопку, чтобы получить новости', reply_markup=markup)

if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)