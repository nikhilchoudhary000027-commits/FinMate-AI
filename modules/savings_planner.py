"""Savings goals and required-saving estimates (amounts in integer paise)."""

from datetime import date, datetime
from math import ceil

from database.db import get_connection
from modules.financial_calculations import rupees_to_paise


def months_remaining(target_date, today=None):
    """Whole calendar months from today to target_date (minimum 0)."""
    today = today or date.today()
    months = (target_date.year - today.year) * 12 + (target_date.month - today.month)
    if target_date.day < today.day:
        months -= 1
    return max(months, 0)


def calculate_goal_progress(target_paise, saved_paise, target_date, today=None):
    """Return progress figures for one goal. Estimates only, no returns assumed."""
    today = today or date.today()
    remaining = max(target_paise - saved_paise, 0)
    percent = round(min(saved_paise * 100 / target_paise, 100), 1)
    months = months_remaining(target_date, today)

    if remaining == 0:
        status = "achieved"
        monthly_required = 0
    elif target_date <= today:
        status = "overdue"
        monthly_required = None
    else:
        status = "in_progress"
        monthly_required = ceil(remaining / max(months, 1))

    return {
        "remaining_paise": remaining,
        "percent": percent,
        "months_remaining": months,
        "monthly_required_paise": monthly_required,
        "status": status,
    }


def add_goal(user_id, goal_name, target_text, saved_text, target_date_text):
    """Create a savings goal. Returns (success, message)."""
    if not goal_name or not goal_name.strip():
        return False, "Goal name is required."
    target_paise = rupees_to_paise(target_text)
    if target_paise is None:
        return False, "Target amount must be greater than 0."
    saved_text = str(saved_text).strip()
    saved_paise = 0 if saved_text in ("", "0") else rupees_to_paise(saved_text)
    if saved_paise is None:
        return False, "Saved amount must be 0 or a positive number."
    try:
        target_date = datetime.strptime(str(target_date_text), "%Y-%m-%d").date()
    except ValueError:
        return False, "Target date must be in YYYY-MM-DD format."
    if target_date <= date.today():
        return False, "Target date must be in the future."

    conn = get_connection()
    try:
        conn.execute(
            "INSERT INTO savings_goals (user_id, goal_name, target_paise, "
            "saved_paise, target_date) VALUES (?, ?, ?, ?, ?)",
            (user_id, goal_name.strip(), target_paise, saved_paise, str(target_date)),
        )
        conn.commit()
        return True, "Goal added."
    finally:
        conn.close()


def list_goals(user_id):
    """Return the user's goals with progress figures."""
    conn = get_connection()
    try:
        rows = conn.execute(
            "SELECT id, goal_name, target_paise, saved_paise, target_date "
            "FROM savings_goals WHERE user_id = ? ORDER BY target_date",
            (user_id,),
        ).fetchall()
    finally:
        conn.close()

    goals = []
    for r in rows:
        goal = dict(r)
        target_date = datetime.strptime(goal["target_date"], "%Y-%m-%d").date()
        goal.update(calculate_goal_progress(
            goal["target_paise"], goal["saved_paise"], target_date))
        goals.append(goal)
    return goals


def update_saved_amount(user_id, goal_id, saved_text):
    """Set the amount saved so far for the user's own goal."""
    saved_text = str(saved_text).strip()
    saved_paise = 0 if saved_text in ("", "0") else rupees_to_paise(saved_text)
    if saved_paise is None:
        return False, "Saved amount must be 0 or a positive number."
    conn = get_connection()
    try:
        cur = conn.execute(
            "UPDATE savings_goals SET saved_paise = ? WHERE id = ? AND user_id = ?",
            (saved_paise, goal_id, user_id),
        )
        conn.commit()
        if cur.rowcount == 0:
            return False, "Goal not found."
        return True, "Saved amount updated."
    finally:
        conn.close()


def delete_goal(user_id, goal_id):
    """Delete the user's own goal."""
    conn = get_connection()
    try:
        cur = conn.execute(
            "DELETE FROM savings_goals WHERE id = ? AND user_id = ?",
            (goal_id, user_id),
        )
        conn.commit()
        if cur.rowcount == 0:
            return False, "Goal not found."
        return True, "Goal deleted."
    finally:
        conn.close()