"""Monthly budgets and alert status for FinMate AI (amounts in integer paise)."""

import re

from database.db import get_connection
from modules.financial_calculations import (
    category_spending, rupees_to_paise, total_by_type,
)
from modules.transactions import CATEGORIES, list_transactions

MONTH_PATTERN = re.compile(r"^\d{4}-(0[1-9]|1[0-2])$")
OVERALL = "Overall"


def set_budget(user_id, month, category, limit_text):
    """Create or update a budget. Returns (success, message)."""
    if not MONTH_PATTERN.match(str(month)):
        return False, "Month must be in YYYY-MM format."
    if category != OVERALL and category not in CATEGORIES:
        return False, "Please choose a valid category."
    limit_paise = rupees_to_paise(limit_text)
    if limit_paise is None:
        return False, "Budget must be a number greater than 0."

    conn = get_connection()
    try:
        conn.execute(
            "INSERT INTO budgets (user_id, category, month, limit_paise) "
            "VALUES (?, ?, ?, ?) "
            "ON CONFLICT (user_id, category, month) "
            "DO UPDATE SET limit_paise = excluded.limit_paise",
            (user_id, category, month, limit_paise),
        )
        conn.commit()
        return True, "Budget saved."
    finally:
        conn.close()


def get_budgets(user_id, month):
    """Return the user's budgets for a month as a list of dicts."""
    conn = get_connection()
    try:
        rows = conn.execute(
            "SELECT category, limit_paise FROM budgets "
            "WHERE user_id = ? AND month = ?",
            (user_id, month),
        ).fetchall()
        return [dict(r) for r in rows]
    finally:
        conn.close()


def budget_status(user_id, month, warn_percent=80):
    """Compare spending with budgets for one month.

    status is 'ok', 'warning' (>= warn_percent) or 'exceeded' (>= 100).
    Integer arithmetic is used for the comparison; percent_used is for display.
    """
    transactions = list_transactions(
        user_id, start_date=f"{month}-01", end_date=f"{month}-31")
    spent_by_category = category_spending(transactions)
    total_spent = total_by_type(transactions, "expense")

    results = []
    for budget in get_budgets(user_id, month):
        limit = budget["limit_paise"]
        if budget["category"] == OVERALL:
            spent = total_spent
        else:
            spent = spent_by_category.get(budget["category"], 0)

        if spent * 100 >= limit * 100:
            status = "exceeded"
        elif spent * 100 >= limit * warn_percent:
            status = "warning"
        else:
            status = "ok"

        results.append({
            "category": budget["category"],
            "limit_paise": limit,
            "spent_paise": spent,
            "remaining_paise": limit - spent,
            "percent_used": round(spent * 100 / limit, 1),
            "status": status,
        })

    results.sort(key=lambda r: (r["category"] != OVERALL, r["category"]))
    return results