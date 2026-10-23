"""What-if simulator (deterministic maths, integer paise)."""

from modules.financial_calculations import category_spending, total_by_type


def monthly_baseline(transactions):
    """Return baseline figures for one month's transactions."""
    income = total_by_type(transactions, "income")
    expense = total_by_type(transactions, "expense")
    return {
        "income": income,
        "expense": expense,
        "savings": income - expense,
        "by_category": category_spending(transactions),
    }


def simulate(baseline, reduce_category=None, reduce_percent=0,
             extra_saving_paise=0, income_change_percent=0, months=6):
    """Apply a hypothetical scenario to the baseline.

    Returns a dict with baseline and scenario figures. Nothing is saved.
    """
    income = baseline["income"]
    expense = baseline["expense"]

    cut = 0
    if reduce_category and reduce_percent > 0:
        spent = baseline["by_category"].get(reduce_category, 0)
        cut = round(spent * reduce_percent / 100)

    new_income = round(income * (100 + income_change_percent) / 100)
    new_expense = expense - cut
    new_savings = new_income - new_expense + extra_saving_paise

    return {
        "baseline_savings": baseline["savings"],
        "scenario_income": new_income,
        "scenario_expense": new_expense,
        "scenario_savings": new_savings,
        "monthly_difference": new_savings - baseline["savings"],
        "category_cut": cut,
        "months": months,
        "baseline_total": baseline["savings"] * months,
        "scenario_total": new_savings * months,
    }