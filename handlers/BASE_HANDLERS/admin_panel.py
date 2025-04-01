from aiogram.types import FSInputFile  # or BufferedInputFile
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram import types, F
from aiogram.filters import Command

from db.CREATE_DB import Session,User,user_output
from utils.utils import users_grafs_to_admin
from utils.config import bot, dp, CHANNEL_ID

from keyboards.admin_panel import admin_panel_keyboard

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
    
    await callback.message.answer("Рассылка!")