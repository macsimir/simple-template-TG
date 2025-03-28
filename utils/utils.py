import matplotlib.pyplot as plt
import pandas as pd
from collections import defaultdict
from datetime import datetime
import matplotlib.ticker as ticker
import sys
from pathlib import Path

# Добавляем корень проекта в PYTHONPATH
project_root = Path(__file__).parent.parent
sys.path.append(str(project_root))

from db.CREATE_DB import session, User, fill_database_with_users

# Заполняем базу данных (если нужно)

def users_grafs_to_admin():
    users = session.query(User).all()
    reg_counts = defaultdict(int)# Создаем словарь для подсчета регистраций по дням
    for user in users:
        date_key = user.date_reg.strftime("%Y-%m-%d")
        reg_counts[date_key] += 1

    # Преобразуем в DataFrame и сортируем по дате
    df = pd.DataFrame({
        'Дата регистрации': list(reg_counts.keys()),
        'Количество регистраций': list(reg_counts.values())
    })
    df['Дата регистрации'] = pd.to_datetime(df['Дата регистрации'])
    df = df.sort_values('Дата регистрации')

    # Настройка стиля
    plt.style.use('seaborn-v0_8')  # Более современный стиль
    plt.figure(figsize=(12, 6))

    # Линейный график с маркерами
    plt.plot(
        df['Дата регистрации'], 
        df['Количество регистраций'], 
        linestyle='-',          # Сплошная линия
        linewidth=2,            # Толщина линии
        color='#4C72B0',        # Приятный синий цвет
        markersize=8,           # Размер точек
        label='Регистрации'     # Легенда
    )

    # Заголовки и подписи
    plt.title('Динамика регистраций по дням', fontsize=16, pad=20)
    plt.xlabel('Дата', fontsize=12)
    plt.ylabel('Количество регистраций', fontsize=12)
    plt.xticks(rotation=45)
    plt.grid(True, linestyle='--', alpha=0.6)  # Сетка

    # Форматирование оси Y (только целые числа)
    plt.gca().yaxis.set_major_locator(ticker.MaxNLocator(integer=True))

    # Улучшенное отображение дат
    plt.gca().xaxis.set_major_formatter(plt.matplotlib.dates.DateFormatter('%Y-%m-%d'))

    # Автоподбор размера и сохранение
    plt.tight_layout()
    plt.savefig('utils/img/registrations_line_chart.jpg', dpi=300, bbox_inches='tight', format='jpeg')
    plt.close()
