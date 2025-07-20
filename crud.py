# db/crud.py

from sqlmodel import Session, select
from db.models import Task, User
from datetime import datetime, timezone
import time

# =====================================================
# USERS
# =====================================================

def create_user(db: Session, telegram_id: int, username: str):
    """
    Створити користувача, якщо його ще немає.
    Якщо username змінився – оновити.
    """
    user = db.exec(select(User).where(User.telegram_id == telegram_id)).first()
    if not user:
        new_user = User(telegram_id=telegram_id, username=username)
        db.add(new_user)
        db.commit()
        db.refresh(new_user)
        return new_user
    else:
        if user.username != username:
            user.username = username
            db.commit()
            db.refresh(user)
        return user


def get_user_by_telegram_id(db: Session, telegram_id: int):
    """
    Отримати користувача за telegram_id.
    """
    return db.exec(select(User).where(User.telegram_id == telegram_id)).first()


def update_username(db: Session, telegram_id: int, new_username: str):
    """
    Оновити username користувача.
    """
    user = get_user_by_telegram_id(db, telegram_id)
    if user:
        user.username = new_username
        db.commit()
        db.refresh(user)
    return user

# =====================================================
# TASKS
# =====================================================

def create_task(db: Session, user_id: int, name: str):
    start_time = int(time.time())
    
    new_task = Task(
        user_id=user_id,
        name=name,
        start_time=start_time
    )
    db.add(new_task)
    db.commit()
    db.refresh(new_task)
    return new_task


def get_tasks_by_user(db: Session, user_id: int):
    """
    Отримати всі завдання користувача.
    """
    tasks = db.exec(select(Task).where(Task.user_id == user_id)).all()
    return tasks


def get_task_by_id(db: Session, task_id: int):
    """
    Отримати завдання за його ID.
    """
    return db.exec(select(Task).where(Task.id == task_id)).first()


def update_task(db: Session, task_id: int, **kwargs):
    """
    🔧 Оновлює завдання в БД.

    ➡️ Приклад виклику:
        update_task(db, 5, end_time=datetime.now(), duration=30)

    📌 Параметри:
    - db: сесія БД
    - task_id: ID завдання
    - kwargs: пари ключ-значення для оновлення
    """

    # Отримати task за id
    task = get_task_by_id(db, task_id)
    if not task:
        return None

    # Оновити поля
    for key, value in kwargs.items():
        if hasattr(task, key):
            setattr(task, key, value)
        else:
            raise ValueError(f"Task has no attribute '{key}'")

    db.commit()
    db.refresh(task)
    return task


def delete_task(db: Session, task_id: int):
    """
    Видалити завдання за ID.
    """
    task = get_task_by_id(db, task_id)
    if not task:
        return None

    db.delete(task)
    db.commit()
    return True



def get_active_task_by_user(db: Session, user_id: int):
    statement = select(Task).where(
        (Task.user_id == user_id) & (Task.end_time == None)
    ).limit(1)

    result = db.exec(statement).first()
    return result
