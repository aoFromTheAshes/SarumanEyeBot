from aiogram.filters import Command
from aiogram import types, Router
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from datetime import datetime, timezone
import time

import crud
from db.db import engine
from sqlmodel import Session


# /START
async def start_command(message: types.Message):
    user_id = message.from_user.id
    user = message.from_user.username
    with Session(engine) as db:
        crud.create_user(db=db, telegram_id=user_id, username=user)
    
    await message.answer("Wellcome to the Sarumans eye!")

# /ADD
class AddTask(StatesGroup):
    waiting_for_task_name = State()
    waiting_for_task_type = State()
    waiting_for_duration = State()



async def add_command(message: types.Message, state: FSMContext):
    await message.answer("Enter task name:")
    await state.set_state(AddTask.waiting_for_task_name)


async def process_task_name(message: types.Message, state: FSMContext):
    await state.update_data(task_name=message.text)

    # Кнопки вибору типу
    keyboard = ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text="Exact duration")],
            [KeyboardButton(text="Free tracking")]
        ],
        resize_keyboard=True,
        one_time_keyboard=True
    )
    await message.answer("Choose tracking type:", reply_markup=keyboard)
    await state.set_state(AddTask.waiting_for_task_type)

async def process_task_type(message: types.Message, state: FSMContext):
    data = await state.get_data()
    task_name = data["task_name"]

    if message.text == "Exact duration":
        await message.answer("Enter duration in minutes:", reply_markup=types.ReplyKeyboardRemove())
        await state.set_state(AddTask.waiting_for_duration)

    elif message.text == "Free tracking":
        # Створюємо task з start_time зараз
        with Session(engine) as db:
            user = crud.get_user_by_telegram_id(db=db, telegram_id=message.from_user.id)
            if not user:
                await message.answer("User not found in DB.")
                return
            
            crud.create_task(
                db=db,
                user_id=user.id,
                name=task_name,
            )
        await message.answer("Task with free tracking started ✅", reply_markup=types.ReplyKeyboardRemove())
        await state.clear()
    else:
        await message.answer("Please choose from keyboard options.")


async def process_duration(message: types.Message, state: FSMContext):
    data = await state.get_data()
    task_name = data["task_name"]

    try:
        duration = int(message.text)
    except ValueError:
        await message.answer("Please enter a valid number in minutes.")
        return

    with Session(engine) as db:
        crud.create_task(
            db=db,
            user_id=message.from_user.id,
            name=task_name,
            duration=duration
        )

    await message.answer(f"Task '{task_name}' with duration {duration} min created ✅")
    await state.clear()


# /LIST
async def get_list(message: types.Message):
    with Session(engine) as db:
        user = crud.get_user_by_telegram_id(db=db, telegram_id=message.from_user.id)

        if not user:
            await message.answer("User not found in DB.")
            return
        
        
        tasks = crud.get_tasks_by_user(db=db, user_id=user.id)

        if not tasks:
            await message.answer("You don't have any tasks yet.")
            return

        # Форматування
        text = "📝 Your tasks:\n"
        for task in tasks:
            text += f"\n🔹 {task.id}. {task.name} "

            if task.duration:
                text += f"({task.duration} min)"
            elif task.start_time:
                text += f"(started at {task.start_time.strftime('%H:%M:%S')})"

        await message.answer(text)


# /STOP
async def stop_task(message: types.Message):

    with Session(engine) as db:
        user = crud.get_user_by_telegram_id(db=db, telegram_id=message.from_user.id)
        if not user:
            await message.answer("User not found in DB.")
            return

        task = crud.get_active_task_by_user(db=db, user_id=user.id)

        if task is None:
            await message.answer('No active tracking tasks.')
            return

        end_time = int(time.time())
        start_time = task.start_time

        # if start_time.tzinfo is None:
        #     start_time = start_time.replace(tzinfo=timezone.utc)



        duration_seconds = end_time - start_time
        duration_minutes = int(duration_seconds // 60)

        # Онови task
        crud.update_task(
            db=db,
            task_id=task.id,
            end_time=end_time,
            duration=duration_minutes
        )

                # Форматування для відповіді
        start_dt = datetime.fromtimestamp(end_time, tz=timezone.utc)
        end_dt = datetime.fromtimestamp(start_time, tz=timezone.utc)

        await message.answer(
            f"✅ Task '{task.name}' stopped.\n"
            f"Started: {start_dt.strftime('%Y-%m-%d %H:%M:%S %Z')}\n"
            f"Ended: {end_dt.strftime('%Y-%m-%d %H:%M:%S %Z')}\n"
            f"Duration: {duration_minutes} min"
        )
# DELETE
class DeleteTask(StatesGroup):
    waiting_for_task_id = State()

async def delete_command(message: types.Message, state: FSMContext):
    tg_id = message.from_user.id
    with Session(engine) as db:
        tasks = crud.get_tasks_by_user(db=db, user_id=tg_id)

        if not tasks:
            await message.answer("You have no tasks to delete.")
            return

        # Показуємо список з id
        text = "🗑️ Which task do you want to delete? Enter the task ID:\n"
        for task in tasks:
            text += f"{task.id}. {task.name}\n"

        await message.answer(text)
        await state.set_state(DeleteTask.waiting_for_task_id)

async def process_delete_task(message: types.Message, state: FSMContext):
    task_id_text = message.text

    try:
        task_id = int(task_id_text)
    except ValueError:
        await message.answer("Please enter a valid task ID number.")
        return

    with Session(engine) as db:
        success = crud.delete_task(db=db, task_id=task_id)

    if success:
        await message.answer("✅ Task deleted successfully.", reply_markup=types.ReplyKeyboardRemove())
    else:
        await message.answer("❌ Task not found or could not be deleted.")

    await state.clear()










