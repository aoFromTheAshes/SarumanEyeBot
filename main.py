import asyncio
from aiogram.fsm.strategy import FSMStrategy
from aiogram import Bot, Dispatcher, types
from aiogram.filters import Command
from handlers import (
    start_command,
    get_list,
    add_command,
    process_task_name,
    process_task_type,
    process_duration,
    stop_task,
    delete_command,
    process_delete_task,
    AddTask,
    DeleteTask,
)

from db.db import create_tables

import os
from dotenv import load_dotenv


load_dotenv()
create_tables()
API_TOKEN = os.getenv("TOKEN")

# start and list
bot = Bot(token=API_TOKEN)
dp = Dispatcher(fsm_strategy=FSMStrategy.CHAT)

# start and list
dp.message.register(start_command, Command("start"))
dp.message.register(get_list, Command("list"))

# ADD flow (FSM)
dp.message.register(add_command, Command("add"))
dp.message.register(process_task_name, AddTask.waiting_for_task_name)
dp.message.register(process_task_type, AddTask.waiting_for_task_type)
dp.message.register(process_duration, AddTask.waiting_for_duration)

# STOP (звичайний хендлер)
dp.message.register(stop_task, Command("stop"))

# DELETE flow (FSM)
dp.message.register(delete_command, Command("delete"))
dp.message.register(process_delete_task, DeleteTask.waiting_for_task_id)



async def main():
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())    
