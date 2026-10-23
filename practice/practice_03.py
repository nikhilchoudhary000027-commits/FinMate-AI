def total_amount(amounts_paise):
    """Return the sum of a list of paise amounts."""
    total = 0
    for amount in amounts_paise:
        total = total + amount
    return total


def format_rupees(amount_paise):
    """Convert integer paise to a display string like Rs. 180.50."""
    return f"Rs. {amount_paise / 100:.2f}"


expenses = [18000, 25000, 120000]
income = [3000000]

print("Total expenses:", format_rupees(total_amount(expenses)))
print("Total income:", format_rupees(total_amount(income)))
transaction = {
    "date": "2026-10-20",
    "amount_paise": 18000,
    "type": "expense",
    "description": "Lunch at cafe",
    "category": "Food",
}

print(transaction["description"])
print(transaction["amount_paise"])

transactions = [
    transaction,
    {"date": "2026-10-19", "amount_paise": 25000, "type": "expense",
     "description": "Uber ride", "category": "Travel"},
    {"date": "2026-10-01", "amount_paise": 3000000, "type": "income",
     "description": "Salary", "category": "Salary"},
]

expense_amounts = []
for t in transactions:
    if t["type"] == "expense":
        expense_amounts.append(t["amount_paise"])

print("Expense amounts:", expense_amounts)
print("Total expenses:", format_rupees(total_amount(expense_amounts)))