# Telegram Bot Template

Шаблонный бот на aiogram 3 с SQLAlchemy для работы с базой данных. Основные функции:
- Проверка подписки на канал
- Админ-панель с рассылкой и статистикой

## Функционал

- Проверка подписки пользователя на канал
- Админ-панель (`/admin_panel`) с:
  - Рассылкой сообщений всем пользователям
  - Статистикой бота
- Работа с базой данных через SQLAlchemy

## Установка и запуск

1. **Создание виртуального окружения**:
   ```bash
   python -m venv .venv

    Активация на Windows:
    bash

.venv\Scripts\activate

Активация на macOS/Linux:
bash

    source .venv/bin/activate

    Установка зависимостей:
    bash

pip install aiogram python-dotenv sqlalchemy

Или из файла requirements.txt (если создан)

Настройка окружения:
Создайте файл .env в корне проекта:
ini

BOT_TOKEN="1234567890:AAFxTmPqXyZiUQqQqQqQqQqQqQqQqQqQqQq"
ID_ADMIN="9876543210"
DATABASE_URL="sqlite:///database.db"

Где:

    BOT_TOKEN - замените на токен от @BotFather

    ID_ADMIN - ваш Telegram ID (можно узнать у @userinfobot)

    DATABASE_URL - URL для подключения к БД (SQLite по умолчанию)

Запуск бота:
bash

    python main.py

Использование админ-панели

Доступ по команде /admin_panel для пользователя с ID, указанным в ID_ADMIN:

    Рассылка:

        Отправка сообщений всем пользователям бота

    Статистика:

        Просмотр количества пользователей и другой статистики

Требования

    Python 3.8+

    aiogram 3.x

    SQLAlchemy 2.x

    python-dotenv