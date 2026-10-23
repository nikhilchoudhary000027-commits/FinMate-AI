from datetime import date

from modules.anomaly_detection import find_unusual
from modules.authentication import login_user, register_user
from modules.csv_tools import export_csv, import_csv
from modules.savings_planner import calculate_goal_progress
from modules.simulator import simulate
from modules.transactions import list_transactions
from database.db import get_connection


def make_user(username="user_one"):
    ok, msg = register_user("Test User", f"{username}@example.com", username, "Secret123")
    assert ok, msg
    return login_user(username, "Secret123")


def test_savings_progress():
    r = calculate_goal_progress(6000000, 1200000, date(2027, 3, 20), date(2026, 10, 20))
    assert r["remaining_paise"] == 4800000
    assert r["percent"] == 20.0
    assert r["months_remaining"] == 5
    assert r["monthly_required_paise"] == 960000
    assert calculate_goal_progress(100, 100, date(2027, 1, 1), date(2026, 1, 1))["status"] == "achieved"
    assert calculate_goal_progress(100, 10, date(2026, 1, 1), date(2026, 6, 1))["status"] == "overdue"


def test_simulator():
    base = {"income": 5000000, "expense": 3000000, "savings": 2000000,
            "by_category": {"Food": 1000000}}
    r = simulate(base, reduce_category="Food", reduce_percent=15)
    assert r["category_cut"] == 150000
    assert r["scenario_savings"] == 2150000
    assert simulate(base, extra_saving_paise=200000)["scenario_savings"] == 2200000
    assert simulate(base, income_change_percent=-10)["scenario_savings"] == 1500000


def _food(amount, day):
    return {"id": day, "txn_date": f"2026-10-{day:02d}", "amount_paise": amount,
            "txn_type": "expense", "description": "Food", "category": "Food"}


def test_anomaly_detection():
    normal = [_food(a, i + 1) for i, a in enumerate([15000, 18000, 16000, 17000, 19000, 16500])]
    assert find_unusual(normal) == []
    flagged = find_unusual(normal + [_food(250000, 20)])
    assert len(flagged) == 1 and flagged[0]["amount_paise"] == 250000
    assert find_unusual(normal[:3]) == []
    assert find_unusual([_food(10000, d) for d in range(1, 8)]) == []


def test_csv_import_export():
    u = make_user()
    sample = ("date,amount,type,description,category\n"
              "2026-10-10,150.50,expense,Chai,Food\n"
              "2026-10-11,abc,expense,Bad,Food\n"
              "2026-10-12,200,expense,Bad cat,Nonsense\n"
              "2026-10-13,500,income,Gig,Freelance Income\n")
    first = import_csv(u["id"], sample)
    assert first["added"] == 2 and len(first["invalid"]) == 2
    second = import_csv(u["id"], sample)
    assert second["added"] == 0 and second["duplicates"] == 2
    assert "error" in import_csv(u["id"], "a,b\n1,2\n")
    assert len(export_csv(u["id"]).strip().splitlines()) == 3  # header + 2 rows
    assert len(list_transactions(u["id"])) == 2


def test_csv_isolation():
    a, b = make_user("user_a"), make_user("user_b")
    import_csv(a["id"], "date,amount,type,description,category\n2026-10-10,10,expense,Tea,Food\n")
    assert "Tea" not in export_csv(b["id"])


def test_password_hashing_and_injection():
    make_user()
    conn = get_connection()
    row = conn.execute("SELECT password_hash FROM users").fetchone()
    conn.close()
    assert row["password_hash"].startswith("$2b$")
    assert "Secret123" not in row["password_hash"]
    assert login_user("user_one' OR '1'='1", "x") is None
    assert list_transactions(1, search_text="'; DROP TABLE users; --") == []
    conn = get_connection()
    assert conn.execute("SELECT COUNT(*) FROM users").fetchone()[0] == 1
    conn.close()