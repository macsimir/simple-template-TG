import logging #Библиотека для логов
import asyncio #Библиотека для асинхрон.работы
from utils.config import dp,bot

logging.basicConfig(level=logging.INFO) #Пишим логи для бота

async def start_bot():
    from handlers.BASE_HANDLERS import start,help,admin_panel
    logging.info("Запуск бота...")
    await dp.start_polling(bot)


if __name__ == "__main__":
    logging.info("Бот запущен и готов к работе")
    asyncio.run(start_bot())