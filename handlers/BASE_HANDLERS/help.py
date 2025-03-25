from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram import types, F
from aiogram.filters import Command

from utils.config import bot, dp, CHANNEL_ID


@dp.message(Command("help"))
async def help_command(message: types.Message):
    await message.answer("Это бот пример. Для начала введите /start")