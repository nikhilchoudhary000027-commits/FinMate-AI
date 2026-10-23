"""CSV import and export for a single user's transactions."""

import csv
import io

from database.db import get_connection
from modules.transactions import list_transactions, validate_transaction

REQUIRED = ["date", "amount", "type", "description", "category"]


def import_csv(user_id, file_text):
    """Import transactions. Returns a summary dict (nothing fails silently)."""
    reader = csv.DictReader(io.StringIO(file_text))
    if reader.fieldnames is None or any(c not in reader.fieldnames for c in REQUIRED):
        return {"error": f"CSV must have columns: {', '.join(REQUIRED)}"}

    conn = get_connection()
    added, duplicates, invalid = 0, 0, []
    try:
        existing = {
            (r["txn_date"], r["amount_paise"], r["txn_type"], r["description"].lower())
            for r in list_transactions(user_id)
        }
        for line_no, row in enumerate(reader, start=2):
            error, paise = validate_transaction(
                (row["date"] or "").strip(), row["amount"],
                (row["type"] or "").strip().lower(),
                row["description"], (row["category"] or "").strip())
            if error:
                invalid.append(f"Row {line_no}: {error}")
                continue
            key = (row["date"].strip(), paise, row["type"].strip().lower(),
                   row["description"].strip().lower())
            if key in existing:
                duplicates += 1
                continue
            conn.execute(
                "INSERT INTO transactions (user_id, txn_date, amount_paise, txn_type, "
                "description, category) VALUES (?, ?, ?, ?, ?, ?)",
                (user_id, key[0], paise, key[2], row["description"].strip(),
                 row["category"].strip()))
            existing.add(key)
            added += 1
        conn.commit()
    finally:
        conn.close()
    return {"added": added, "duplicates": duplicates, "invalid": invalid}


def export_csv(user_id):
    """Return the user's own transactions as CSV text."""
    out = io.StringIO()
    writer = csv.writer(out)
    writer.writerow(REQUIRED)
    for t in list_transactions(user_id):
        writer.writerow([t["txn_date"], f"{t['amount_paise'] / 100:.2f}",
                         t["txn_type"], t["description"], t["category"]])
    return out.getvalue()