# 🕒 Saruman's Eye – Time Manager Telegram Bot

This is a **Telegram bot for personal task time tracking**, built with:

- [Aiogram](https://docs.aiogram.dev/en/latest/)
- [SQLModel](https://sqlmodel.tiangolo.com/)
- PostgreSQL as database
- uv as dependency and virtual environment manager

---

## 🚀 Features

✅ Add new tasks with **exact duration** or **free tracking mode**  
✅ Stop free-tracked tasks to calculate duration automatically  
✅ List all your current tasks  
✅ Delete tasks by ID

---

## ⚙️ Installation

1. **Clone the repository**

```bash
git clone https://github.com/yourusername/sarumaneyebot.git
cd sarumaneyebot

2. **Install uv if not installed**
pip install uv

3. **Install dependencies**
uv pip install

4. **Set up environment variables**

Create a .env file in the project root:

TOKEN=your_telegram_bot_token
DB_NAME=your_database_name
DB_USER=your_database_user
DB_PASS=your_database_password
DB_PORT=5432
DB_HOST=localhost

5. **Create database tables**

Ensure PostgreSQL is running, then:

uv run python -c "from db.db import create_tables; create_tables()"

▶️ Run the bot
uv run python main.py

💡 Notes
Uses pyproject.toml for dependency management (no requirements.txt needed).

Uses uv for fast and isolated virtual environment management.

Adjust timezone logic if deploying to production with different user timezones.