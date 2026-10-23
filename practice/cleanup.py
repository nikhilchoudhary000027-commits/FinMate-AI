from database.db import get_connection

conn = get_connection()
conn.execute("DELETE FROM transactions")
conn.commit()
print("Test transactions removed.")
conn.close()