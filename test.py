from db.CREATE_DB import Session, User
from datetime import datetime

session = Session()
try:
    # Получаем всех пользователей
    users = session.query(User).all()
    
    # Выводим заголовок таблицы
    print(f"{'ID':<5} | {'Telegram ID':<12} | {'Privilege':<10} | {'Date Reg'}")
    print("-" * 50)
    
    # Выводим данные каждого пользователя
    for user in users:
        # Форматируем дату для красивого вывода
        reg_date = user.date_reg.strftime('%Y-%m-%d') if user.date_reg else 'None'
        print(f"{user.user_id:<5} | {user.telegram_id:<12} | {user.privilege or 'None':<10} | {reg_date}")
        
finally:
    # Всегда закрываем сессию
    session.close()


