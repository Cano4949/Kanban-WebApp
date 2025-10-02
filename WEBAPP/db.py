# db.py
import sqlite3
from pathlib import Path
from typing import Optional

DB_PATH = Path("kanban.db")

def get_conn():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

def init_db_users():
    conn = get_conn()
    conn.executescript("""
    PRAGMA foreign_keys = ON;
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT NOT NULL UNIQUE,
        password TEXT NOT NULL,
        created_at DATETIME DEFAULT CURRENT_TIMESTAMP
    );
    """)
    conn.commit()
    conn.close()

def create_user(username: str, password: str) -> Optional[int]:
    conn = get_conn()
    try:
        conn.execute(
            "INSERT INTO users(username, password) VALUES(?,?)",
            (username, password)
        )
        conn.commit()
        return conn.execute("SELECT last_insert_rowid() AS id").fetchone()["id"]
    except sqlite3.IntegrityError:
        return None
    finally:
        conn.close()

def find_user_by_username(username: str):
    conn = get_conn()
    row = conn.execute("SELECT * FROM users WHERE username = ?", (username,)).fetchone()
    conn.close()
    return row

def check_login(username: str, password: str) -> Optional[int]:
    u = find_user_by_username(username)
    if not u:
        return None
    return u["id"] if u["password"] == password else None
