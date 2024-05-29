import sqlite3

conn = sqlite3.connect('auth.db', check_same_thread=False)
cursor = conn.cursor()

def init_db():
    sql = """CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY,
        username TEXT NOT NULL UNIQUE,
        email TEXT NOT NULL,
        password TEXT NOT NULL
    )"""
    cursor.execute(sql)
    conn.commit()

def get_db():
    return conn