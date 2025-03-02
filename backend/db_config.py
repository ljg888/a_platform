import sqlite3
import os

# 确保db目录存在
os.makedirs('db', exist_ok=True)

DB_PATH = 'db/test_configs.db'

def get_db_connection():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn
