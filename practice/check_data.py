from database.db import get_connection

conn = get_connection()
rows = conn.execute("SELECT id, description, amount_paise FROM transactions").fetchall()
print("Rows in database:", len(rows))
for r in rows:
    print(dict(r))
conn.close()