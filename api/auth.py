import os
import sqlite3
import jwt
import hashlib
from datetime import datetime, timedelta
from dotenv import load_dotenv

load_dotenv()

DB_PATH = "tool_calls.db"
JWT_SECRET = os.getenv("JWT_SECRET", "ganesh_secret")
JWT_ALGORITHM = "HS256"


def init_auth_db():
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()

    cur.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            password_hash TEXT NOT NULL,
            role TEXT NOT NULL DEFAULT 'user',
            created_at TEXT NOT NULL
        )
    """)

    conn.commit()
    conn.close()


def hash_password(password):
    return hashlib.sha256(password.encode("utf-8")).hexdigest()


def create_user(username, password, role="user"):
    init_auth_db()

    username = username.strip()
    password = password.strip()
    role = role.strip().lower()

    if not username or not password:
        return False, "Username and password required"

    if role not in ["admin", "user"]:
        role = "user"

    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()

    cur.execute("SELECT id FROM users WHERE username=?", (username,))
    if cur.fetchone():
        conn.close()
        return False, "User already exists"

    cur.execute("""
        INSERT INTO users (username, password_hash, role, created_at)
        VALUES (?, ?, ?, ?)
    """, (
        username,
        hash_password(password),
        role,
        datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    ))

    conn.commit()
    conn.close()

    return True, "User created successfully"


def authenticate_user(username, password):
    init_auth_db()

    username = username.strip()
    password = password.strip()

    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()

    cur.execute("""
        SELECT username, password_hash, role
        FROM users
        WHERE username=?
    """, (username,))

    row = cur.fetchone()
    conn.close()

    if not row:
        return None

    db_username, password_hash, role = row

    if hash_password(password) != password_hash:
        return None

    return {
        "username": db_username,
        "role": role
    }


def create_token(user):
    payload = {
        "sub": user["username"],
        "role": user["role"],
        "exp": datetime.utcnow() + timedelta(hours=8)
    }

    return jwt.encode(payload, JWT_SECRET, algorithm=JWT_ALGORITHM)


def verify_token(token):
    try:
        return jwt.decode(token, JWT_SECRET, algorithms=[JWT_ALGORITHM])
    except Exception:
        return None