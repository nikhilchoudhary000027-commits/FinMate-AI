"""FinMate chatbot: intent model + entity extraction + deterministic handlers."""

from datetime import date
from pathlib import Path

import joblib

from modules.budget_planner import OVERALL, budget_status
from modules.categorization import predict_category
from modules.financial_calculations import (
    category_spending, format_rupees, total_by_type,
)
from modules.nlp_utils import (
    extract_amount_paise, extract_category, extract_date, extract_month,
    extract_percent,
)
from modules.transactions import add_transaction, list_transactions

INTENT_MODEL_PATH = Path(__file__).resolve().parent.parent / "models" / "intent_classifier.joblib"
INTENT_CONFIDENCE_THRESHOLD = 0.30

_intent_model = None


def _load_intent_model():
    global _intent_model
    if _intent_model is None and INTENT_MODEL_PATH.exists():
        _intent_model = joblib.load(INTENT_MODEL_PATH)
    return _intent_model


def detect_intent(text):
    """Return (intent, confidence). Low confidence -> 'unsupported'."""
    model = _load_intent_model()
    if model is None:
        return "unsupported", None
    proba = model.predict_proba([text])[0]
    best = proba.argmax()
    confidence = float(proba[best])
    if confidence < INTENT_CONFIDENCE_THRESHOLD:
        return "unsupported", confidence
    return str(model.classes_[best]), confidence


def _month_transactions(user_id, month):
    return list_transactions(user_id, start_date=f"{month}-01", end_date=f"{month}-31")


def handle_message(user_id, text, pending=None):
    """Process one message.

    pending: a dict describing an expense awaiting confirmation, or None.
    Returns (reply_text, new_pending).
    """
    clean = text.strip()
    lower = clean.lower()

    # ---- Confirmation step for a pending expense ----
    if pending is not None:
        if lower in ("yes", "y", "confirm", "ok", "haan", "ha"):
            ok, msg = add_transaction(
                user_id, pending["date"], str(pending["amount_paise"] / 100),
                "expense", pending["description"], pending["category"])
            if ok:
                return (f"Saved: {format_rupees(pending['amount_paise'])} under "
                        f"{pending['category']} on {pending['date']}."), None
            return f"Could not save: {msg}", None
        if lower in ("no", "n", "cancel", "nahi"):
            return "Okay, I did not save it.", None
        return "Please reply 'yes' to save or 'no' to cancel.", pending

    if not clean:
        return "Please type a question about your finances.", None

    intent, _ = detect_intent(clean)
    category = extract_category(clean)
    month = extract_month(clean)

    # Rule that corrects a known weakness: a category word means category_spend.
    if intent == "spend_total" and category:
        intent = "category_spend"

    # ---- Intents that need data ----
    if intent == "spend_total":
        txns = _month_transactions(user_id, month)
        return f"Your recorded spending for {month} is {format_rupees(total_by_type(txns, 'expense'))}.", None

    if intent == "top_category":
        spending = category_spending(_month_transactions(user_id, month))
        if not spending:
            return f"No expenses recorded for {month}.", None
        name, amount = next(iter(spending.items()))
        return f"Your biggest expense category in {month} is {name} at {format_rupees(amount)}.", None

    if intent == "category_spend":
        if not category:
            return "Which category do you mean (for example food, travel, shopping)?", None
        spent = category_spending(_month_transactions(user_id, month)).get(category, 0)
        return f"You spent {format_rupees(spent)} on {category} in {month}.", None

    if intent == "budget_check":
        statuses = budget_status(user_id, month)
        if not statuses:
            return f"You have not set any budgets for {month}.", None
        lines = []
        for s in statuses:
            lines.append(f"{s['category']}: {format_rupees(s['spent_paise'])} of "
                         f"{format_rupees(s['limit_paise'])} ({s['percent_used']}%, {s['status']})")
        return "Budget status for " + month + ":\n" + "\n".join(lines), None

    if intent == "savings_month":
        txns = _month_transactions(user_id, month)
        saved = total_by_type(txns, "income") - total_by_type(txns, "expense")
        return (f"Recorded income minus expenses for {month} is {format_rupees(saved)}. "
                "This is calculated from your records, not a bank balance."), None

    if intent == "what_if_reduce":
        percent = extract_percent(clean)
        if not category or percent is None or not 0 < percent <= 100:
            return ("Please tell me a category and a percentage, for example: "
                    "'reduce shopping by 20 percent'."), None
        spent = category_spending(_month_transactions(user_id, month)).get(category, 0)
        saving = round(spent * percent / 100)
        return (f"This month you spent {format_rupees(spent)} on {category}. "
                f"Reducing it by {percent:g}% would save about {format_rupees(saving)}. "
                "This is an estimate, not a guarantee."), None

    if intent == "add_expense":
        amount = extract_amount_paise(clean)
        if amount is None:
            return "I could not find an amount. Please include one, for example 'add 250 for Uber'.", None
        suggested, _, _ = predict_category(clean)
        pending_new = {
            "amount_paise": amount,
            "category": suggested if suggested != "Salary" else "Other",
            "date": extract_date(clean),
            "description": clean,
        }
        return (f"I understood: expense of {format_rupees(amount)}, category "
                f"{pending_new['category']}, date {pending_new['date']}. "
                "Reply 'yes' to save or 'no' to cancel."), pending_new

    return ("Sorry, I can only answer questions about your spending, categories, budget, "
            "savings, what-if reductions, and adding expenses."), None