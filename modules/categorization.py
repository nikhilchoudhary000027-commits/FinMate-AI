"""Expense categorisation: rule-based baseline and TF-IDF + Logistic Regression."""

KEYWORD_RULES = {
    "Food": ["lunch", "dinner", "breakfast", "zomato", "swiggy", "grocery",
             "restaurant", "cafe", "tea", "milk", "snacks"],
    "Travel": ["uber", "ola", "cab", "metro", "train", "bus", "petrol",
               "flight", "auto", "ticket to"],
    "Shopping": ["amazon", "flipkart", "myntra", "shoes", "mall", "bought"],
    "Rent": ["rent"],
    "Education": ["tuition", "course", "exam", "textbook", "coaching", "udemy"],
    "Healthcare": ["doctor", "medicine", "pharmacy", "dental", "hospital", "lab"],
    "Bills and Utilities": ["electricity", "recharge", "broadband", "bill", "gas", "dth"],
    "Entertainment": ["movie", "netflix", "spotify", "concert", "game"],
    "Salary": ["salary", "paycheck", "pay received"],
    "Freelance Income": ["freelance", "client", "consulting", "tutoring"],
}


def rule_based_category(description):
    """Return the first category whose keyword appears, else 'Other'."""
    text = description.lower()
    for category, keywords in KEYWORD_RULES.items():
        if any(word in text for word in keywords):
            return category
    return "Other"

from pathlib import Path

import joblib

MODEL_PATH = Path(__file__).resolve().parent.parent / "models" / "expense_classifier.joblib"
CONFIDENCE_THRESHOLD = 0.40

_model = None

def _load_model():
    """Load the saved pipeline once. Returns None if the file is missing."""
    global _model
    if _model is None and MODEL_PATH.exists():
        _model = joblib.load(MODEL_PATH)
    return _model


def predict_category(description):
    """Return (category, confidence, source).

    source is 'model' when the ML model is confident enough, otherwise
    'fallback' (rules, then 'Other'). confidence is None if no model is available.
    """
    if not description or not description.strip():
        return "Other", None, "fallback"

    model = _load_model()
    if model is None:
        return rule_based_category(description), None, "fallback"

    probabilities = model.predict_proba([description])[0]
    best = probabilities.argmax()
    confidence = float(probabilities[best])
    if confidence >= CONFIDENCE_THRESHOLD:
        return str(model.classes_[best]), round(confidence, 3), "model"
    return rule_based_category(description), round(confidence, 3), "fallback"