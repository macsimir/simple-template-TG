from sqlalchemy import create_engine, Column, Integer, String, Date
from sqlalchemy.orm import sessionmaker, declarative_base, relationship
from sqlalchemy.exc import SQLAlchemyError
from dotenv import load_dotenv 
from datetime import datetime

import os
import logging 


logging.basicConfig(level=logging.INFO)

Base = declarative_base()
engine = create_engine('sqlite:///DATABASE.db')
Session = sessionmaker(bind=engine)
session = Session()

class User(Base):
    __tablename__ = 'users'
    user_id = Column(Integer, primary_key=True)
    telegram_id = Column(Integer, unique=True)  # Added unique constraint
    privilege = Column(String)
    date_reg = Column(Date, default=datetime.utcnow)
    
    @classmethod
    def exists_by_telegram_id(cls, session, telegram_id):
        return session.query(cls).filter(cls.telegram_id == telegram_id).first() is not None

def create_new_user(session, telegram_id, privilege):
    if not User.exists_by_telegram_id(session, telegram_id):
        try:
            new_user = User(telegram_id=telegram_id, privilege=privilege)
            session.add(new_user)
            session.commit()
            logging.info(f"Пользователь {telegram_id} успешно создан")
            return True
        except SQLAlchemyError as e:
            session.rollback()
            logging.error(f"Ошибка в создание пользователя {telegram_id}: {str(e)}")
            return False
    else:
        logging.info(f"Пользователь {telegram_id} уже существует")
        return False

def user_output():
    users = session.query(User).all()
    return '\n'.join(f'{u.user_id}-{u.telegram_id}:{u.privilege}' for u in users)


from sqlalchemy.orm import sessionmaker
from datetime import datetime, timedelta
import random
def fill_database_with_users(count=100, same_day_count=4):    
    
    # Список возможных привилегий
    privileges = ['user']
    
    # Генерируем дату для same_day_count пользователей
    special_date = datetime.now() - timedelta(days=random.randint(1, 31))
    
    for i in range(1, count + 1):
        # Для первых same_day_count пользователей используем special_date
        if i <= same_day_count:
            reg_date = special_date.date()
        else:
            reg_date = (datetime.now() - timedelta(days=random.randint(1, 365))).date()
        
        user = User(
            telegram_id=100000 + i,  # Уникальный ID для каждого пользователя
            privilege=random.choice(privileges),
            date_reg=reg_date
        )
        session.add(user)
    
    session.commit()
    session.close()
    print(f"База данных заполнена {count} пользователями, {same_day_count} из которых зарегистрированы в один день.")

if __name__ == "__main__":
    load_dotenv()
    Base.metadata.create_all(engine)
    
    id_admin = os.getenv("ID_ADMIN")
    create_new_user(session=session, telegram_id=int(id_admin), privilege="admin")

    # fill_database_with_users()