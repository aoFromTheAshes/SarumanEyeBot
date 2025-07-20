import pytest
from sqlmodel import SQLModel, create_engine, Session
from db.models import User
from crud import create_user, get_user_by_telegram_id

# Створюємо окремий engine для тестів (SQLite in-memory)
engine = create_engine("sqlite:///:memory:", echo=True)

# Фікстура для бази даних
@pytest.fixture()
def session():
    SQLModel.metadata.create_all(engine)
    with Session(engine) as session:
        yield session

def test_create_user(session):
    telegram_id = 12345
    username = "testuser"

    # Викликаємо твою CRUD функцію
    create_user(session, telegram_id=telegram_id, username=username)

    # Перевіряємо
    user = get_user_by_telegram_id(session, telegram_id)
    assert user is not None
    assert user.telegram_id == telegram_id
    assert user.username == username
