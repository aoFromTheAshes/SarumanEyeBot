from dotenv import load_dotenv
import os
from .models import User, Task

load_dotenv(dotenv_path=r"C:\Users\vchep\Desktop\SEXY_codes\SarumanEyeBot\.env")


# DB_HOST = os.environ.get("DB_HOST")
# DB_PORT = os.environ.get("DB_PORT")
# DB_NAME = os.environ.get("DB_NAME")
# DB_USER = os.environ.get("DB_USER")
# DB_PASS = os.environ.get("DB_PASS")
DATABASE_URL = os.environ.get("DATABASE_URL")