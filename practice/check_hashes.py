from database.db import get_connection

conn = get_connection()
for r in conn.execute("SELECT id, username, substr(password_hash, 1, 7) AS prefix FROM users"):
    print(r["id"], r["username"], r["prefix"])
conn.close()