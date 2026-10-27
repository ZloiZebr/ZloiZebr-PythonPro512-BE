from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, DeclarativeBase


# Строка подключения для SQLite
DATABASE_URL = "sqlite:///cryshopa.db"

# Создаём Engine
engine = create_engine(DATABASE_URL, echo=True) # echo=True - включить логирование всех SQL-запросов прямо в консоль нашего приложения

# Настраиваем фабрику сессий
SessionLocal = sessionmaker(bind=engine) # Создаём фабрику, а не сессию


# Определяем базовый класс для моделей
class Base(DeclarativeBase):
  pass
