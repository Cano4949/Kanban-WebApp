# db.py
import sqlite3
from pathlib import Path
from typing import Optional, List, Dict

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

    CREATE TABLE IF NOT EXISTS columns (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        position INTEGER NOT NULL DEFAULT 0,
        project_id INTEGER NOT NULL,
        FOREIGN KEY(project_id) REFERENCES projects(id) ON DELETE CASCADE
    );

    CREATE TABLE IF NOT EXISTS cards (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        title TEXT NOT NULL,
        description TEXT,
        position INTEGER NOT NULL DEFAULT 0,
        column_id INTEGER NOT NULL,
        assignee_id INTEGER,
        created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY(column_id) REFERENCES columns(id) ON DELETE CASCADE,
        FOREIGN KEY(assignee_id) REFERENCES users(id) ON DELETE SET NULL
    );
    """)
    conn.commit()
    conn.close()

def create_user(username: str, password: str) -> Optional[int]:
    conn = get_conn()
    try:
        conn.execute("INSERT INTO users(username, password) VALUES(?,?)", (username, password))
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
    if not u: return None
    return u["id"] if u["password"] == password else None

def create_project(name: str, owner_id: int) -> int:
    conn = get_conn()
    cur = conn.cursor()
    cur.execute("INSERT INTO projects(name) VALUES(?)", (name,))
    pid = cur.lastrowid
    cur.execute("INSERT INTO project_members(user_id, project_id, role) VALUES(?,?, 'owner')", (owner_id, pid))

    for i, cname in enumerate(["To Do", "In Progress", "Review", "Done"]):
        cur.execute("INSERT INTO columns(name, position, project_id) VALUES(?,?,?)", (cname, i, pid))
    conn.commit()
    conn.close()
    return pid


def list_user_projects(user_id: int):
    conn = get_conn()
    rows = conn.execute("""
      SELECT p.* FROM projects p
      JOIN project_members m ON m.project_id = p.id
      WHERE m.user_id = ?
      ORDER BY p.created_at ASC
    """, (user_id,)).fetchall()
    conn.close()
    return rows

def get_project(project_id: int):
    conn = get_conn()
    p = conn.execute("SELECT * FROM projects WHERE id = ?", (project_id,)).fetchone()
    conn.close()
    return p

def is_member(user_id: int, project_id: int) -> bool:
    conn = get_conn()
    row = conn.execute("SELECT 1 FROM project_members WHERE user_id=? AND project_id=?", (user_id, project_id)).fetchone()
    conn.close()
    return row is not None

def add_member(project_id: int, username: str) -> bool:
    u = find_user_by_username(username)
    if not u: return False
    uid = u["id"]
    conn = get_conn()
    try:
        conn.execute("INSERT INTO project_members(user_id, project_id) VALUES(?,?)", (uid, project_id))
        conn.commit()
        return True
    except sqlite3.IntegrityError:
        return True  
    finally:
        conn.close()

def project_members(project_id: int):
    conn = get_conn()
    rows = conn.execute("""
      SELECT u.* FROM users u
      JOIN project_members m ON m.user_id = u.id
      WHERE m.project_id = ?
      ORDER BY u.username ASC
    """, (project_id,)).fetchall()
    conn.close()
    return rows

def list_columns(project_id: int):
    conn = get_conn()
    rows = conn.execute("SELECT * FROM columns WHERE project_id=? ORDER BY position ASC", (project_id,)).fetchall()
    conn.close()
    return rows

def create_column(project_id: int, name: str):
    conn = get_conn()
    cur = conn.cursor()
    maxpos = cur.execute("SELECT COALESCE(MAX(position), -1) FROM columns WHERE project_id=?", (project_id,)).fetchone()[0]
    cur.execute("INSERT INTO columns(name, position, project_id) VALUES(?,?,?)", (name, maxpos+1, project_id))
    conn.commit(); conn.close()

def rename_column(column_id: int, name: str):
    conn = get_conn()
    conn.execute("UPDATE columns SET name=? WHERE id=?", (name, column_id))
    conn.commit(); conn.close()

def delete_column(column_id: int):
    conn = get_conn()
    pid_row = conn.execute("SELECT project_id FROM columns WHERE id=?", (column_id,)).fetchone()
    if not pid_row: conn.close(); return
    pid = pid_row[0]
    conn.execute("DELETE FROM columns WHERE id=?", (column_id,))
    rows = conn.execute("SELECT id FROM columns WHERE project_id=? ORDER BY position ASC", (pid,)).fetchall()
    for i, r in enumerate(rows):
        conn.execute("UPDATE columns SET position=? WHERE id=?", (i, r["id"]))
    conn.commit(); conn.close()

def list_cards_by_column(project_id: int) -> Dict[int, List[sqlite3.Row]]:
    conn = get_conn()
    cols = conn.execute("SELECT id FROM columns WHERE project_id=? ORDER BY position", (project_id,)).fetchall()
    mapping = {c["id"]: [] for c in cols}
    if cols:
        placeholders = ",".join(["?"] * len(cols))
        rows = conn.execute(f"""
            SELECT c.*, u.username AS assignee_name
            FROM cards c
            LEFT JOIN users u ON u.id = c.assignee_id
            WHERE c.column_id IN ({placeholders})
            ORDER BY c.position ASC
        """, [c["id"] for c in cols]).fetchall()
        for r in rows:
            mapping[r["column_id"]].append(r)
    conn.close()
    return mapping

def create_card(column_id: int, title: str, description: str, assignee_id: Optional[int]):
    conn = get_conn()
    cur = conn.cursor()
    maxpos = cur.execute("SELECT COALESCE(MAX(position), -1) FROM cards WHERE column_id=?", (column_id,)).fetchone()[0]
    cur.execute("INSERT INTO cards(title, description, position, column_id, assignee_id) VALUES(?,?,?,?,?)",
                (title, description, maxpos+1, column_id, assignee_id))
    conn.commit(); conn.close()

def update_card(card_id: int, title: str, description: str, assignee_id: Optional[int]):
    conn = get_conn()
    conn.execute("UPDATE cards SET title=?, description=?, assignee_id=? WHERE id=?",
                 (title, description, assignee_id, card_id))
    conn.commit(); conn.close()

def delete_card(card_id: int):
    conn = get_conn()
    col_row = conn.execute("SELECT column_id FROM cards WHERE id=?", (card_id,)).fetchone()
    if not col_row: conn.close(); return
    col_id = col_row[0]
    conn.execute("DELETE FROM cards WHERE id=?", (card_id,))
    rows = conn.execute("SELECT id FROM cards WHERE column_id=? ORDER BY position ASC", (col_id,)).fetchall()
    for i, r in enumerate(rows):
        conn.execute("UPDATE cards SET position=? WHERE id=?", (i, r["id"]))
    conn.commit(); conn.close()

def move_card(card_id: int, to_column_id: int):
    """No-JS move: append to end of the target column."""
    conn = get_conn()
    cur = conn.cursor()
    row = cur.execute("SELECT column_id FROM cards WHERE id=?", (card_id,)).fetchone()
    if not row:
        conn.close(); return
    old_col = row[0]

    others = cur.execute("SELECT id FROM cards WHERE column_id=? AND id<>? ORDER BY position", (old_col, card_id)).fetchall()
    for i, r in enumerate(others):
        cur.execute("UPDATE cards SET position=? WHERE id=?", (i, r["id"]))

    maxpos = cur.execute("SELECT COALESCE(MAX(position), -1) FROM cards WHERE column_id=?", (to_column_id,)).fetchone()[0]
    cur.execute("UPDATE cards SET column_id=?, position=? WHERE id=?", (to_column_id, maxpos+1, card_id))
    conn.commit(); conn.close()

def is_owner(user_id: int, project_id: int) -> bool:
    conn = get_conn()
    row = conn.execute(
        "SELECT 1 FROM project_members WHERE user_id=? AND project_id=? AND role='owner'",
        (user_id, project_id)
    ).fetchone()
    conn.close()
    return row is not None

def delete_project(project_id: int):
    """Deletes the project. Thanks to FOREIGN KEYs with ON DELETE CASCADE,
    this also deletes memberships, columns, and cards."""
    conn = get_conn()
    conn.execute("DELETE FROM projects WHERE id=?", (project_id,))
    conn.commit()
    conn.close()