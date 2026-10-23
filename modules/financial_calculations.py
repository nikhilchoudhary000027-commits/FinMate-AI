"""Money helpers and core financial calculations (all amounts in integer paise)."""

from decimal import Decimal, InvalidOperation, ROUND_HALF_UP
from collections import defaultdict

def rupees_to_paise(amount_text):
    """Convert user input (str/int/float) in rupees to integer paise.

    Uses Decimal so that values like 180.50 never suffer float rounding errors.
    Returns None if the input is not a valid positive amount.
    """
    try:
        value = Decimal(str(amount_text).strip())
    except (InvalidOperation, ValueError):
        return None
    if not value.is_finite() or value <= 0:
        return None
    paise = (value * 100).quantize(Decimal("1"), rounding=ROUND_HALF_UP)
    return int(paise)


def format_rupees(amount_paise):
    """Convert integer paise to a display string like Rs. 1,234.50."""
    return f"Rs. {amount_paise / 100:,.2f}"

def total_by_type(transactions, txn_type):
    """Sum of amount_paise for one transaction type."""
    return sum(t["amount_paise"] for t in transactions if t["txn_type"] == txn_type)


def calculate_balance(transactions):
    """Calculated balance = income - expenses (NOT a bank-confirmed balance)."""
    return total_by_type(transactions, "income") - total_by_type(transactions, "expense")


def category_spending(transactions):
    """Return {category: total_paise} for expenses only, largest first."""
    totals = defaultdict(int)
    for t in transactions:
        if t["txn_type"] == "expense":
            totals[t["category"]] += t["amount_paise"]
    return dict(sorted(totals.items(), key=lambda item: item[1], reverse=True))


def monthly_summary(transactions):
    """Return {'YYYY-MM': {'income': paise, 'expense': paise, 'savings': paise}}."""
    months = defaultdict(lambda: {"income": 0, "expense": 0})
    for t in transactions:
        month = t["txn_date"][:7]
        months[month][t["txn_type"]] += t["amount_paise"]
    result = {}
    for month in sorted(months):
        income = months[month]["income"]
        expense = months[month]["expense"]
        result[month] = {"income": income, "expense": expense, "savings": income - expense}
    return result