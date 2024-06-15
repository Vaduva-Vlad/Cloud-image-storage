import sqlite3

conn = sqlite3.connect('process.db', check_same_thread=False)
cursor = conn.cursor()

def init_db():
    sql = """CREATE TABLE IF NOT EXISTS history (
        id INTEGER PRIMARY KEY,
        user_id TEXT NOT NULL,
        image_name TEXT,
        date_modified TEXT
    )"""
    cursor.execute(sql)
    conn.commit()

def get_db():
    return conn