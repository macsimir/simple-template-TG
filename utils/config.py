from aiogram import Bot, Dispatcher
from aiogram import Bot,Dispatcher
from dotenv import load_dotenv
import os 

load_dotenv()

BOT_TOKEN = os.getenv('BOT_TOKEN')
CHANNEL_ID = "@macsimomg"
bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()
