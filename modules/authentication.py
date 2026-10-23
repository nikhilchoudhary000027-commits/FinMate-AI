"""User registration and login for FinMate AI."""

import re
import sqlite3

import bcrypt

from database.db import get_connection

EMAIL_PATTERN = re.compile(r"^[^@\s]+@[^@\s]+\.[^@\s]+$")
USERNAME_PATTERN = re.compile(r"^[A-Za-z0-9_]{3,20}$")


def validate_registration(name, email, username, password):
    """Return an error message string, or None if all inputs are valid."""
    if not name or not name.strip():
        return "Name is required."
    if not EMAIL_PATTERN.match(email.strip()):
        return "Enter a valid email address."
    if not USERNAME_PATTERN.match(username.strip()):
        return "Username must be 3-20 characters: letters, digits or underscore."
    if len(password) < 8:
        return "Password must be at least 8 characters."
    if not (any(c.isalpha() for c in password) and any(c.isdigit() for c in password)):
        return "Password must contain at least one letter and one digit."
    return None


def register_user(name, email, username, password):
    """Create a new user. Returns (success: bool, message: str)."""
    error = validate_registration(name, email, username, password)
    if error:
        return False, error

    password_hash = bcrypt.hashpw(password.encode("utf-8"), bcrypt.gensalt()).decode("utf-8")

    conn = get_connection()
    try:
        conn.execute(
            "INSERT INTO users (name, email, username, password_hash) VALUES (?, ?, ?, ?)",
            (name.strip(), email.strip().lower(), username.strip().lower(), password_hash),
        )
        conn.commit()
        return True, "Registration successful. Please log in."
    except sqlite3.IntegrityError:
        return False, "That email or username is already registered."
    finally:
        conn.close()


def login_user(username, password):
    """Check credentials. Returns a user dict (id, name, username) or None."""
    conn = get_connection()
    try:
        row = conn.execute(
            "SELECT id, name, username, password_hash FROM users WHERE username = ?",
            (username.strip().lower(),),
        ).fetchone()
    finally:
        conn.close()

    if row is None:
        return None
    if bcrypt.checkpw(password.encode("utf-8"), row["password_hash"].encode("utf-8")):
        return {"id": row["id"], "name": row["name"], "username": row["username"]}
    return None