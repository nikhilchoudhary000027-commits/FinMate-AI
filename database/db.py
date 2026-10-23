"""Database helper functions for FinMate AI (SQLite)."""

import sqlite3
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
DB_PATH = BASE_DIR / "finmate.db"
SCHEMA_PATH = Path(__file__).resolve().parent / "schema.sql"


def get_connection():
    """Open a connection with foreign keys enabled and dict-like rows."""
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA foreign_keys = ON;")
    return conn


def init_db():
    """Create tables from schema.sql if they do not exist (safe to re-run)."""
    with open(SCHEMA_PATH, "r", encoding="utf-8") as f:
        schema = f.read()
    conn = get_connection()
    try:
        conn.executescript(schema)
        conn.commit()
    finally:
        conn.close()


if __name__ == "__main__":
    init_db()
    print("Database initialised at:", DB_PATH)