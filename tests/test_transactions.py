from modules.authentication import register_user, login_user
from modules.transactions import (add_transaction, update_transaction,
                                  delete_transaction, list_transactions)
from modules.financial_calculations import rupees_to_paise

# Money conversion
print(rupees_to_paise("180.50"), rupees_to_paise("abc"), rupees_to_paise("-5"), rupees_to_paise("0"))

# Two users
register_user("Ravi Kumar", "ravi@example.com", "ravi_01", "Secret123")
asha = login_user("asha_01", "Secret123")
ravi = login_user("ravi_01", "Secret123")

# Asha adds
print(add_transaction(asha["id"], "2026-10-20", "180", "expense", "Lunch", "Food"))
print(add_transaction(asha["id"], "2026-10-01", "30000", "income", "Salary", "Salary"))
print(add_transaction(asha["id"], "2026-10-20", "-50", "expense", "Bad", "Food"))
print(add_transaction(asha["id"], "2030-01-01", "50", "expense", "Future", "Food"))

asha_rows = list_transactions(asha["id"])
print("Asha rows:", len(asha_rows))
print("Ravi rows:", len(list_transactions(ravi["id"])))

# Isolation: Ravi tries to delete Asha's transaction
first_id = asha_rows[0]["id"]
print(delete_transaction(ravi["id"], first_id))
print(update_transaction(ravi["id"], first_id, "2026-10-20", "1", "expense", "Hack", "Food"))
print("Asha rows after Ravi's attempt:", len(list_transactions(asha["id"])))

# Asha edits and deletes her own
print(update_transaction(asha["id"], first_id, "2026-10-20", "200", "expense", "Lunch", "Food"))
print(delete_transaction(asha["id"], first_id))
print("Asha rows at end:", len(list_transactions(asha["id"])))