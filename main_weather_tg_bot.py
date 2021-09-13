from config import weather_token, tg_bot_token
import requests
import datetime
from aiogram import Bot, types
from aiogram.dispatcher import Dispatcher
from aiogram.utils import executor

bot = Bot(token=tg_bot_token)
dp = Dispatcher(bot)

@dp.message_handler(commands=['start'])
async def start_command(message: types.Message):
	await message.reply("Привет! Напиши мне название города, и я пришлю сводку погоды!")

@dp.message_handler()
async def get_weather(message: types.Message):
	weather_emoji = {"Clear": "Ясно \U00002600",
					 "Clouds": "Облачно \U00002601",
					 "Snow": "Снег \U0001F328",
					 "Rain": "Дождь \U00002614",
					 "Drizzle": "Дождь \U00002614",
					 "Thunderstorm": "Гроза \U000026A1",
					 "Mist": "Туман \U0001F328"
					 }
	try:
		r = requests.get(
			f"http://api.openweathermap.org/data/2.5/weather?q={message.text}&appid={weather_token}&units=metric"
		)
		data = r.json()

		weather_discription = data['weather'][0]['main']
		if weather_discription in weather_emoji:
			wd = weather_emoji[weather_discription]
		else:
			wd = "Не понимаю, что там на улице, выгляни в окно!"

		city = data['name']
		cur_weather = data['main']['temp']
		humidity = data['main']['humidity']
		pressure = data['main']['pressure']
		wind = data['wind']['speed']
		sunrise = datetime.datetime.fromtimestamp(data['sys']['sunrise'])
		sunset = datetime.datetime.fromtimestamp(data['sys']['sunset'])
		length_sun_day = datetime.datetime.fromtimestamp(data['sys']['sunset']) - datetime.datetime.fromtimestamp(
			data['sys']['sunrise'])

		await message.reply(f'***{datetime.datetime.now().strftime("%Y-%m-%d %H:%M")}***\n'
			  f'Погода в городе: {city}\nТемпература: {cur_weather}°С {wd}\n'
			  f'Влажность: {humidity}%\nАтмосферное давление: {pressure} мм.рт.ст\n'
			  f'Скорость ветра: {wind} м/с\nВремя рассвета: {sunrise}\n'
			  f'Время заката: {sunset}\nПродолжительность светового дня: {length_sun_day}\n'
			  f' \U0001F525 Где еще хотите узнать погоду? \U0001F525')
	except:
		await message.reply('\U000026D4 Проверьте название города \U000026D4')

if __name__ == '__main__':
	executor.start_polling(dp)