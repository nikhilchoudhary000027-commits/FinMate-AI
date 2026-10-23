from database.db import init_db, get_connection

init_db()
conn = get_connection()

# ---- CREATE: a temporary test user ----
conn.execute(
    "INSERT OR IGNORE INTO users (name, email, username, password_hash) "
    "VALUES (?, ?, ?, ?)",
    ("Test User", "test@example.com", "testuser", "not-a-real-hash"),
)
conn.commit()

user_id = conn.execute(
    "SELECT id FROM users WHERE username = ?", ("testuser",)
).fetchone()["id"]
print("User id:", user_id)

# ---- CREATE: insert a transaction ----
cursor = conn.execute(
    "INSERT INTO transactions "
    "(user_id, txn_date, amount_paise, txn_type, description, category) "
    "VALUES (?, ?, ?, ?, ?, ?)",
    (user_id, "2026-10-20", 18000, "expense", "Lunch at cafe", "Food"),
)
conn.commit()
txn_id = cursor.lastrowid
print("Inserted transaction id:", txn_id)

# ---- READ ----
rows = conn.execute(
    "SELECT id, txn_date, amount_paise, description, category "
    "FROM transactions WHERE user_id = ?",
    (user_id,),
).fetchall()
for row in rows:
    print(row["id"], row["txn_date"], row["amount_paise"], row["description"], row["category"])

# ---- UPDATE ----
conn.execute(
    "UPDATE transactions SET amount_paise = ? WHERE id = ? AND user_id = ?",
    (20000, txn_id, user_id),
)
conn.commit()
updated = conn.execute(
    "SELECT amount_paise FROM transactions WHERE id = ? AND user_id = ?",
    (txn_id, user_id),
).fetchone()
print("After update:", updated["amount_paise"])

# ---- DELETE ----
# conn.execute(
#     "DELETE FROM transactions WHERE id = ? AND user_id = ?",
#     (txn_id, user_id),
# )
# conn.commit()
# count = conn.execute(
#     "SELECT COUNT(*) AS c FROM transactions WHERE user_id = ?", (user_id,)
# ).fetchone()["c"]
# print("Transactions left:", count)

conn.close()