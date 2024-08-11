import logging
from aiogram import Bot, Dispatcher, executor, types
import gspread
from oauth2client.service_account import ServiceAccountCredentials

# Настройка логирования
logging.basicConfig(level=logging.INFO)

# Введите ваш токен бота
API_TOKEN = 'YOUR_TELEGRAM_BOT_API_TOKEN'

# Настройка бота и диспетчера
bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot)

# Авторизация в Google Sheets
scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
creds = ServiceAccountCredentials.from_json_keyfile_name("path/to/your/credentials.json", scope)
client = gspread.authorize(creds)
sheet = client.open("YOUR_GOOGLE_SHEET_NAME").sheet1  # Откройте лист

@dp.message_handler(commands=['start', 'help'])
async def send_welcome(message: types.Message):
    await message.reply("Привет! Отправь мне сообщение, и я сохраню его в Google Sheets.")

@dp.message_handler()
async def save_message(message: types.Message):
    user = message.from_user
    data = [user.id, user.username, user.first_name, user.last_name, message.text]

    # Добавление строки в Google Sheet
    sheet.append_row(data)

    await message.reply("Ваше сообщение сохранено в Google Sheets!")

if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
