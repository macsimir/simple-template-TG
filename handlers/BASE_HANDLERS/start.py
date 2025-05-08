from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram import types, F
from aiogram.filters import Command
from db.CREATE_DB import create_new_user,Session,User
from utils.config import bot, dp, CHANNEL_ID
import time

@dp.message(Command("start"))
async def help_command(message: types.Message):
    session = Session()
    telegram_id = message.chat.id
    user = session.query(User).filter(User.telegram_id == telegram_id).first()
    if user:
        user_channel_status = await bot.get_chat_member(chat_id=CHANNEL_ID, user_id=message.from_user.id)
        if user_channel_status.status != "left":
            await message.answer(f"Спасибо что ты подписан!")
        else:
            await message.answer(f"Подпишись {CHANNEL_ID}")
    else:
        create_new_user(session=session,telegram_id=telegram_id, privilege='user')
        user_channel_status = await bot.get_chat_member(chat_id=CHANNEL_ID, user_id=message.from_user.id)
        if user_channel_status.status != "left":
            await message.answer(f"Спасибо что ты подписан!")
        else:
            await message.answer(f"Подпишись {CHANNEL_ID}")

