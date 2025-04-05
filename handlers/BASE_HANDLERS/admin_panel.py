from aiogram.types import FSInputFile  # or BufferedInputFile
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram import types, F,exceptions
from aiogram.filters import Command

from db.CREATE_DB import Session,User,user_output
from utils.utils import users_grafs_to_admin
from utils.config import bot, dp, CHANNEL_ID

from keyboards.admin_panel import admin_panel_keyboard

import time 
import asyncio

@dp.message(Command("admin_panel"))
async def help_command(message: types.Message):
    session = Session() 
    telegram_id = message.chat.id
    user = session.query(User).filter(User.telegram_id == telegram_id).first()
    if user.privilege == "admin":
        await message.answer("Привет админ",reply_markup=admin_panel_keyboard())
    else:
        pass 


@dp.callback_query(F.data == "show_users")
async def show_users_callback(callback: types.CallbackQuery):
    await callback.message.answer("Пожалуйста подождите...")
    users_grafs_to_admin()  # Функция, создающая изображение
    photo = FSInputFile('utils/img/registrations_line_chart.jpg')
    await callback.message.answer_photo(photo=photo, caption="Общая статистика")

@dp.callback_query(F.data == "newsletter")
async def newsletter_callback(callback: types.CallbackQuery):
    session = Session()
    users = session.query(User).all()
    
    failed = 0
    successful = 0

    for user in users:
        try:
            successful += 1
            await bot.send_message(chat_id=user.telegram_id, text="Тестова рассылка")
        except exceptions.TelegramBadRequest as e:
            failed += 1

    report = [
    f"📊 Результат рассылки:",
    f"✅ Успешно: {successful}",
    f"❌ Не удалось: {failed}"
    ]
    await callback.message.answer("\n".join(report))
