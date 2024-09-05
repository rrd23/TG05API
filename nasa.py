import asyncio
from aiogram import Bot, Dispatcher, F
from aiogram.filters import CommandStart, Command
from aiogram.types import Message
import random
import requests
from datetime import datetime, timedelta


from config import TOKEN, NASA_API_KEY

bot = Bot(token=TOKEN)
dp = Dispatcher()



def get_random_apod():
   end_date = datetime.now() # конечная дата - сегодня
   start_date = end_date - timedelta(days=365) # начальная дата - 30 дней назад
   # генерируем случайный даты в пределах года
   random_date = start_date + (end_date - start_date) * random.random()
   random_date_str = random_date.strftime("%Y-%m-%d")

   # делаем запрос к API NASA
   response = requests.get(f"https://api.nasa.gov/planetary/apod?api_key={NASA_API_KEY}&date={random_date_str}")
   data = response.json()
   return data


# обработка команды /random_apod

@dp.message(Command("random_apod"))
async def random_apod(message: Message):
   apod = get_random_apod()
   photo_url = apod['url']
   title = apod['title']

   await message.answer_photo(photo=photo_url, caption=f"{title}")







async def main():
   await dp.start_polling(bot)

if __name__ == '__main__':
   asyncio.run(main())