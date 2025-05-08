from aiogram.types import FSInputFile, InlineKeyboardMarkup, InlineKeyboardButton
from aiogram import types, F, exceptions
from aiogram.filters import Command, StateFilter
from aiogram.fsm.state import StatesGroup, State
from aiogram.fsm.context import FSMContext
from aiogram.fsm.storage.memory import MemoryStorage

from db.CREATE_DB import Session, User, user_output
from utils.utils import users_grafs_to_admin
from utils.config import bot, dp, CHANNEL_ID
from keyboards.admin_panel import admin_panel_keyboard

import time
import asyncio


@dp.message(Command("admin_panel"))
async def help_command(message: types.Message):
    """Обработчик входа в админ-панель"""
    session = Session()
    telegram_id = message.chat.id
    user = session.query(User).filter(User.telegram_id == telegram_id).first()
    
    if user.privilege == "admin":
        welcome_msg = (
            "👋 Добро пожаловать в админ-панель!\n"
            "Здесь вы можете управлять ботом и просматривать статистику.\n"
            "Выберите нужный раздел:"
        )
        await message.answer(welcome_msg, reply_markup=admin_panel_keyboard())
    else:
        await message.answer("⛔ У вас нет прав доступа к этой команде.")


@dp.callback_query(F.data == "show_users")
async def show_users_callback(callback: types.CallbackQuery):
    """Показ статистики пользователей"""
    processing_msg = (
        "📊 Загружаю статистику пользователей...\n"
        "Пожалуйста, подождите 10-15 секунд."
    )
    await callback.message.answer(processing_msg)
    
    users_grafs_to_admin()
    photo = FSInputFile('utils/img/registrations_line_chart.jpg')
    
    stats_msg = (
        "📈 Статистика регистраций пользователей\n"
        "На графике отображена динамика роста пользовательской базы."
    )
    await callback.message.answer_photo(photo=photo, caption=stats_msg)


class Form(StatesGroup):
    """Состояния для создания рассылки"""
    img = State()
    caption = State()
    keyboards = State()
    keyboards_url = State()


@dp.callback_query(F.data == "newsletter")
async def newsletter_callback(callback: types.CallbackQuery, state: FSMContext):
    """Начало создания рассылки"""
    instructions = (
        "📨 Вы начали создание рассылки.\n\n"
        "Шаг 1 из 4: Отправьте изображение для рассылки.\n"
        "Можно отправить как фото, так и картинку."
    )
    await state.set_state(Form.img)
    await callback.message.answer(instructions)


@dp.message(StateFilter(Form.img), F.content_type == 'photo')
async def process_photo(message: types.Message, state: FSMContext):
    """Обработка изображения для рассылки"""
    photo = message.photo[-1]
    await state.update_data(img=photo.file_id)
    
    next_step = (
        "✅ Изображение успешно загружено!\n\n"
        "Шаг 2 из 4: Введите текст сообщения для рассылки.\n"
        "Вы можете использовать форматирование (жирный, курсив и т.д.)."
    )
    await message.answer(next_step)
    await state.set_state(Form.caption)


@dp.message(Form.caption)
async def captions_text(message: types.Message, state: FSMContext):
    """Обработка текста рассылки"""
    await state.update_data(caption=message.text)
    
    keyboard_prompt = (
        "✅ Текст сообщения сохранен!\n\n"
        "Шаг 3 из 4: Нужна ли кнопка в сообщении?\n"
        "- Если да, введите текст для кнопки\n"
        "- Если нет, напишите 'НЕТ'"
    )
    await message.answer(keyboard_prompt)
    await state.set_state(Form.keyboards)


@dp.message(Form.keyboards)
async def state_keybord(message: types.Message, state: FSMContext):
    """Обработка текста кнопки"""
    await state.update_data(keyboards=message.text)
    
    if message.text.upper() != "НЕТ":
        url_instructions = (
            "✅ Текст кнопки сохранен!\n\n"
            "Шаг 4 из 4: Отправьте ссылку для кнопки.\n"
            "Ссылка должна начинаться с http:// или https://"
        )
        await message.answer(url_instructions)
        await state.set_state(Form.keyboards_url)
    else:
        await state.update_data(keyboards_url="")
        await confirm_newsletter(message, state)


@dp.message(Form.keyboards_url)
async def state_keybord_url(message: types.Message, state: FSMContext):
    """Обработка ссылки для кнопки"""
    if not message.text.startswith(('http://', 'https://')):
        error_msg = (
            "❌ Неверный формат ссылки!\n"
            "Пожалуйста, отправьте корректную ссылку, "
            "которая начинается с http:// или https://\n"
            "Попробуйте еще раз."
        )
        await message.answer(error_msg)
        return
    
    await state.update_data(keyboards_url=message.text)
    await confirm_newsletter(message, state)


async def confirm_newsletter(message: types.Message, state: FSMContext):
    """Подтверждение рассылки"""
    data = await state.get_data()
    
    # Создаем клавиатуру если нужно
    keyboard = None
    if data["keyboards"].upper() != "НЕТ" and data["keyboards_url"]:
        buttons = [[
            InlineKeyboardButton(
                text=data["keyboards"], 
                url=data["keyboards_url"]
            )
        ]]
        keyboard = InlineKeyboardMarkup(inline_keyboard=buttons)
    
    preview_msg = (
        "📋 Предпросмотр рассылки:\n"
        "Вот как будет выглядеть ваше сообщение для пользователей."
    )
    await message.answer(preview_msg)
    
    await message.answer_photo(
        photo=data["img"],
        caption=data["caption"],
        reply_markup=keyboard
    )
    
    confirmation_msg = (
        "❓ Вы хотите отправить эту рассылку всем пользователям?\n"
        "Пожалуйста, проверьте все данные перед отправкой."
    )
    confirm_buttons = [
        [
            InlineKeyboardButton(text="✅ Да, отправить", callback_data="Yes"),
            InlineKeyboardButton(text="❌ Нет, отменить", callback_data="No")
        ]
    ]
    confirm_keyboard = InlineKeyboardMarkup(inline_keyboard=confirm_buttons)
    
    await message.answer(confirmation_msg, reply_markup=confirm_keyboard)


@dp.callback_query(F.data == "Yes")
async def yes_command_cal(callback: types.CallbackQuery, state: FSMContext):
    """Отправка рассылки"""
    data = await state.get_data()
    
    # Создаем клавиатуру если нужно
    keyboard = None
    if data["keyboards"].upper() != "НЕТ" and data["keyboards_url"]:
        buttons = [[
            InlineKeyboardButton(
                text=data["keyboards"], 
                url=data["keyboards_url"]
            )
        ]]
        keyboard = InlineKeyboardMarkup(inline_keyboard=buttons)
    
    session = Session()
    users = session.query(User).all()
    
    progress_msg = await callback.message.answer(
        "⏳ Начинаю рассылку...\n"
        "Это может занять некоторое время в зависимости "
        "от количества пользователей."
    )
    
    failed = 0
    successful = 0

    for user in users:
        try:
            await bot.send_photo(
                chat_id=user.telegram_id,
                photo=data["img"],
                caption=data["caption"],
                reply_markup=keyboard
            )
            successful += 1
        except exceptions.TelegramBadRequest:
            failed += 1

    report = (
        "📊 Отчет о рассылке:\n\n"
        f"• Всего пользователей: {len(users)}\n"
        f"• Успешно отправлено: ✅ {successful}\n"
        f"• Не удалось отправить: ❌ {failed}\n\n"
        "Рассылка завершена!"
    )
    
    await progress_msg.delete()
    await callback.message.answer(report)
    await state.clear()


@dp.callback_query(F.data == "No")
async def no_command_cal(callback: types.CallbackQuery, state: FSMContext):
    """Отмена рассылки"""
    await state.clear()
    await callback.message.answer(
        "❌ Рассылка отменена.\n"
        "Все данные удалены. Вы можете начать заново."
    )