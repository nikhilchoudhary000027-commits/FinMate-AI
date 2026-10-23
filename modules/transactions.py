"""Transaction CRUD for FinMate AI. Every query is scoped to user_id."""

from datetime import datetime

from database.db import get_connection
from modules.financial_calculations import rupees_to_paise

CATEGORIES = [
    "Food", "Travel", "Shopping", "Rent", "Education", "Healthcare",
    "Bills and Utilities", "Entertainment", "Salary", "Freelance Income", "Other",
]
TXN_TYPES = ["income", "expense"]


def validate_transaction(txn_date, amount_text, txn_type, description, category):
    """Return (error_message_or_None, amount_paise_or_None)."""
    try:
        parsed = datetime.strptime(str(txn_date), "%Y-%m-%d").date()
    except ValueError:
        return "Date must be in YYYY-MM-DD format.", None
    if parsed > datetime.now().date():
        return "Transaction date cannot be in the future.", None

    amount_paise = rupees_to_paise(amount_text)
    if amount_paise is None:
        return "Amount must be a number greater than 0.", None

    if txn_type not in TXN_TYPES:
        return "Type must be income or expense.", None
    if not description or not description.strip():
        return "Description is required.", None
    if category not in CATEGORIES:
        return "Please choose a valid category.", None
    return None, amount_paise


def add_transaction(user_id, txn_date, amount_text, txn_type, description,
                    category, payment_method=None, notes=None):
    """Insert a transaction. Returns (success, message)."""
    error, amount_paise = validate_transaction(
        txn_date, amount_text, txn_type, description, category)
    if error:
        return False, error
    conn = get_connection()
    try:
        conn.execute(
            "INSERT INTO transactions (user_id, txn_date, amount_paise, txn_type, "
            "description, category, payment_method, notes) "
            "VALUES (?, ?, ?, ?, ?, ?, ?, ?)",
            (user_id, str(txn_date), amount_paise, txn_type, description.strip(),
             category, payment_method, notes),
        )
        conn.commit()
        return True, "Transaction added."
    finally:
        conn.close()


def update_transaction(user_id, txn_id, txn_date, amount_text, txn_type,
                       description, category, payment_method=None, notes=None):
    """Update one of the user's own transactions. Returns (success, message)."""
    error, amount_paise = validate_transaction(
        txn_date, amount_text, txn_type, description, category)
    if error:
        return False, error
    conn = get_connection()
    try:
        cur = conn.execute(
            "UPDATE transactions SET txn_date = ?, amount_paise = ?, txn_type = ?, "
            "description = ?, category = ?, payment_method = ?, notes = ? "
            "WHERE id = ? AND user_id = ?",
            (str(txn_date), amount_paise, txn_type, description.strip(), category,
             payment_method, notes, txn_id, user_id),
        )
        conn.commit()
        if cur.rowcount == 0:
            return False, "Transaction not found."
        return True, "Transaction updated."
    finally:
        conn.close()


def delete_transaction(user_id, txn_id):
    """Delete one of the user's own transactions. Returns (success, message)."""
    conn = get_connection()
    try:
        cur = conn.execute(
            "DELETE FROM transactions WHERE id = ? AND user_id = ?",
            (txn_id, user_id),
        )
        conn.commit()
        if cur.rowcount == 0:
            return False, "Transaction not found."
        return True, "Transaction deleted."
    finally:
        conn.close()


def list_transactions(user_id, start_date=None, end_date=None, category=None,
                      search_text=None):
    """Return the user's transactions (newest first) as a list of dicts."""
    query = ("SELECT id, txn_date, amount_paise, txn_type, description, category, "
             "payment_method, notes FROM transactions WHERE user_id = ?")
    params = [user_id]
    if start_date:
        query += " AND txn_date >= ?"
        params.append(str(start_date))
    if end_date:
        query += " AND txn_date <= ?"
        params.append(str(end_date))
    if category:
        query += " AND category = ?"
        params.append(category)
    if search_text:
        query += " AND description LIKE ?"
        params.append(f"%{search_text.strip()}%")
    query += " ORDER BY txn_date DESC, id DESC"

    conn = get_connection()
    try:
        return [dict(r) for r in conn.execute(query, params).fetchall()]
    finally:
        conn.close()