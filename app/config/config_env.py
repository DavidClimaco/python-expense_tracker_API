import os
from enum import Enum

from dotenv import load_dotenv

load_dotenv()


class EnvironmentVariables(str, Enum):
    SECRET_KEY = os.getenv("SECRET_KEY")
    ALGORITHM = os.getenv("ALGORITHM")
    DATABASE_NAME = os.getenv("DATABASE_NAME")
    DATABASE_USER = os.getenv("DATABASE_USER")
    DATABASE_PASSWORD = os.getenv("DATABASE_PASSWORD")
    DATABASE_PORT = os.getenv("DATABASE_PORT")
    DATABASE_URL = os.getenv("DATABASE_URL")
