from database.db import get_connection
from modules.authentication import login_user, register_user
from modules.transactions import add_transaction, list_transactions, delete_transaction

# 1. Passwords must not be stored in plain text
conn = get_connection()
rows = conn.execute(
    "SELECT username, password_hash FROM users WHERE username != 'testuser'"
).fetchall()
conn.close()
print("Any plain-text 'Secret123' stored?",
      any("Secret123" in r["password_hash"] for r in rows))
print("All hashes start with $2b$ (bcrypt)?",
      all(r["password_hash"].startswith("$2b$") for r in rows))

# 2. SQL injection attempts must fail safely
print("Injection login:", login_user("asha_01' OR '1'='1", "x"))
print("Injection search rows:", len(list_transactions(1, search_text="'; DROP TABLE users; --")))
conn = get_connection()
print("users table still exists:",
      conn.execute("SELECT COUNT(*) FROM users").fetchone()[0] > 0)
conn.close()

# 3. Isolation: two users cannot see each other's rows
asha = login_user("asha_01", "Secret123")
ravi = login_user("ravi_01", "Secret123")
add_transaction(asha["id"], "2026-10-23", "123", "expense", "Isolation check", "Other")
asha_ids = {t["id"] for t in list_transactions(asha["id"])}
ravi_ids = {t["id"] for t in list_transactions(ravi["id"])}
print("Asha and Ravi share any transaction id?", bool(asha_ids & ravi_ids))
target = max(asha_ids)
print("Ravi deleting Asha's row:", delete_transaction(ravi["id"], target))
print("Asha deleting own row:", delete_transaction(asha["id"], target))