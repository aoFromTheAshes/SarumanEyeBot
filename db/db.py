
from sqlmodel import SQLModel, create_engine, Session
from dotenv import load_dotenv
from sqlalchemy.orm import sessionmaker
# from .create_db import DB_HOST, DB_NAME, DB_PASS, DB_PORT, DB_USER
from .create_db import DATABASE_URL



load_dotenv()

# DATABASE_URL = f"postgresql://{DB_USER}:{DB_PASS}@{DB_HOST}:{DB_PORT}/{DB_NAME}"



engine = create_engine(DATABASE_URL, echo=True)

# Функція для отримання сесії

def create_tables():
    SQLModel.metadata.create_all(engine)