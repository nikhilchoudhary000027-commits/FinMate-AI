from modules.authentication import register_user, login_user
from modules.transactions import add_transaction
from modules.budget_planner import set_budget, budget_status

register_user("Budget User", "budget@example.com", "budget_user", "Secret123")
user = login_user("budget_user", "Secret123")
uid = user["id"]

# Expenses for 2026-10
add_transaction(uid, "2026-10-10", "3500", "expense", "Groceries", "Food")
add_transaction(uid, "2026-10-11", "3500", "expense", "Shoes", "Shopping")
add_transaction(uid, "2026-10-12", "1000", "expense", "Bus pass", "Travel")

# Budgets
print(set_budget(uid, "2026-10", "Overall", "20000"))
print(set_budget(uid, "2026-10", "Food", "4000"))
print(set_budget(uid, "2026-10", "Shopping", "3000"))
print(set_budget(uid, "2026-13", "Food", "100"))
print(set_budget(uid, "2026-10", "Food", "-5"))

for s in budget_status(uid, "2026-10"):
    print(s["category"], s["spent_paise"], s["remaining_paise"],
          f"{s['percent_used']}%", s["status"])