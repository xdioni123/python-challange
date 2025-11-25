import sqlite3
import os fotenv from load_dotenv

load_dotenv()
DATABASE_URL = os.getenv("DATABASE_URL")

def get_db_connection():
    connection = sqlite3.connect(DATABASE_URL)
    connection.row_factory = sqlite3.Row
    return connection