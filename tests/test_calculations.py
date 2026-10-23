from modules.financial_calculations import (
    calculate_balance, category_spending, monthly_summary,
    total_by_type, format_rupees,
)

sample = [
    {"txn_date": "2026-09-05", "amount_paise": 3000000, "txn_type": "income", "category": "Salary"},
    {"txn_date": "2026-09-10", "amount_paise": 500000, "txn_type": "expense", "category": "Rent"},
    {"txn_date": "2026-10-01", "amount_paise": 3000000, "txn_type": "income", "category": "Salary"},
    {"txn_date": "2026-10-03", "amount_paise": 18000, "txn_type": "expense", "category": "Food"},
    {"txn_date": "2026-10-05", "amount_paise": 25000, "txn_type": "expense", "category": "Travel"},
    {"txn_date": "2026-10-07", "amount_paise": 199900, "txn_type": "expense", "category": "Shopping"},
    {"txn_date": "2026-10-09", "amount_paise": 12000, "txn_type": "expense", "category": "Food"},
]

print("Income:", format_rupees(total_by_type(sample, "income")))
print("Expense:", format_rupees(total_by_type(sample, "expense")))
print("Balance:", format_rupees(calculate_balance(sample)))
print("Category:", category_spending(sample))
print("Monthly:", monthly_summary(sample))
print("Empty list balance:", calculate_balance([]))