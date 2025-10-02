import sqlite3
from pathlib import Path
from typing import Optional

DB_PATH = Path("kanban.db")

def get_conn():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

def init_db_all():
    conn = get_conn()
    conn.executescript("""
    PRAGMA foreign_keys = ON;

    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT NOT NULL UNIQUE,
        password TEXT NOT NULL,
        created_at DATETIME DEFAULT CURRENT_TIMESTAMP
    );

    CREATE TABLE IF NOT EXISTS projects (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        created_at DATETIME DEFAULT CURRENT_TIMESTAMP
    );

    CREATE TABLE IF NOT EXISTS project_members (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER NOT NULL,
        project_id INTEGER NOT NULL,
        role TEXT DEFAULT 'owner',
        UNIQUE(user_id, project_id),
        FOREIGN KEY(user_id) REFERENCES users(id) ON DELETE CASCADE,
        FOREIGN KEY(project_id) REFERENCES projects(id) ON DELETE CASCADE
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

# --- projects ---
def create_project(name: str, owner_id: int) -> int:
    conn = get_conn()
    cur = conn.cursor()
    cur.execute("INSERT INTO projects(name) VALUES(?)", (name,))
    pid = cur.lastrowid
    cur.execute(
        "INSERT INTO project_members(user_id, project_id, role) VALUES(?,?, 'owner')",
        (owner_id, pid)
    )
    conn.commit()
    conn.close()
    return pid

def list_user_projects(user_id: int):
    conn = get_conn()
    rows = conn.execute("""
      SELECT p.*
      FROM projects p
      JOIN project_members m ON m.project_id = p.id
      WHERE m.user_id = ?
      ORDER BY p.created_at ASC
    """, (user_id,)).fetchall()
    conn.close()
    return rows
