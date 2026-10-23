"""Rule-based entity extraction for the FinMate chatbot."""

import re
from datetime import date, timedelta

from modules.financial_calculations import rupees_to_paise

CATEGORY_WORDS = {
    "Food": ["food", "lunch", "dinner", "breakfast", "grocery", "groceries", "restaurant"],
    "Travel": ["travel", "uber", "ola", "cab", "petrol", "fuel", "metro"],
    "Shopping": ["shopping", "clothes", "shoes", "headphones"],
    "Rent": ["rent"],
    "Education": ["education", "tuition", "course", "books"],
    "Healthcare": ["healthcare", "medicine", "medical", "doctor"],
    "Bills and Utilities": ["bills", "bill", "utilities", "electricity", "recharge"],
    "Entertainment": ["entertainment", "movie", "movies", "netflix"],
}

AMOUNT_PATTERN = re.compile(
    r"(?:rs\.?|rupees|inr|₹)?\s*(\d[\d,]*(?:\.\d{1,2})?)\s*(?:rs\.?|rupees|inr)?",
    re.IGNORECASE,
)
PERCENT_PATTERN = re.compile(r"(\d{1,3}(?:\.\d+)?)\s*(?:%|percent|per cent)", re.IGNORECASE)


def extract_percent(text):
    """Return a percentage as float (e.g. 20.0), or None."""
    match = PERCENT_PATTERN.search(text)
    return float(match.group(1)) if match else None


def extract_amount_paise(text):
    """Return the first amount in paise that is not a percentage, or None."""
    cleaned = PERCENT_PATTERN.sub(" ", text)
    for match in AMOUNT_PATTERN.finditer(cleaned):
        digits = match.group(1).replace(",", "")
        paise = rupees_to_paise(digits)
        if paise is not None:
            return paise
    return None


def extract_category(text):
    """Return the first category whose word appears in the text, or None."""
    words = re.findall(r"[a-z]+", text.lower())
    for category, keywords in CATEGORY_WORDS.items():
        if any(k in words for k in keywords):
            return category
    return None


def extract_month(text, today=None):
    """Return 'YYYY-MM' for 'this month' (default) or 'last month'."""
    today = today or date.today()
    if "last month" in text.lower():
        first_of_this = today.replace(day=1)
        last_month = first_of_this - timedelta(days=1)
        return last_month.strftime("%Y-%m")
    return today.strftime("%Y-%m")


def extract_date(text, today=None):
    """Return an ISO date for 'yesterday', otherwise today."""
    today = today or date.today()
    if "yesterday" in text.lower():
        return (today - timedelta(days=1)).isoformat()
    return today.isoformat()