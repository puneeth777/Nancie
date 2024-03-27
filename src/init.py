import os

from src.config import Config


def init_nancie():
    config = Config()

    print("Initializing Nancie...")
    sqlite_db = config.get_sqlite_db()

    print("Initializing Prerequisites...")
    os.makedirs(os.path.dirname(sqlite_db), exist_ok=True)
