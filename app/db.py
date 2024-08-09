from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

# Создание движка базы данных SQLite
DATABASE_URL = "sqlite:///taskmanager.db"
engine = create_engine(DATABASE_URL, echo=True)

# Создание сессии
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Создание базового класса для моделей
Base = declarative_base()
