from modules.authentication import login_user, register_user
from modules.budget_planner import budget_status, set_budget
from modules.financial_calculations import (
    calculate_balance, category_spending, rupees_to_paise,
)
from modules.transactions import (
    add_transaction, delete_transaction, list_transactions, update_transaction,
)


def make_user(username="user_one"):
    register_user("Test User", f"{username}@example.com", username, "Secret123")
    return login_user(username, "Secret123")


def test_rupees_to_paise():
    assert rupees_to_paise("180.50") == 18050
    assert rupees_to_paise("abc") is None
    assert rupees_to_paise("-5") is None
    assert rupees_to_paise("0") is None


def test_registration_and_login():
    ok, _ = register_user("A B", "a@example.com", "abc_1", "Secret123")
    assert ok
    ok, _ = register_user("A B", "a@example.com", "abc_1", "Secret123")
    assert not ok                       # duplicate
    assert login_user("abc_1", "Secret123") is not None
    assert login_user("abc_1", "wrong123") is None


def test_balance_and_categories():
    u = make_user()
    add_transaction(u["id"], "2026-10-01", "30000", "income", "Salary", "Salary")
    add_transaction(u["id"], "2026-10-02", "180", "expense", "Lunch", "Food")
    add_transaction(u["id"], "2026-10-03", "250", "expense", "Cab", "Travel")
    txns = list_transactions(u["id"])
    assert calculate_balance(txns) == 3000000 - 18000 - 25000
    assert category_spending(txns) == {"Travel": 25000, "Food": 18000}


def test_validation_rejects_bad_input():
    u = make_user()
    assert not add_transaction(u["id"], "2026-10-02", "-50", "expense", "x", "Food")[0]
    assert not add_transaction(u["id"], "2030-01-01", "50", "expense", "x", "Food")[0]
    assert not add_transaction(u["id"], "2026-10-02", "50", "expense", "x", "Nope")[0]
    assert not add_transaction(u["id"], "2026-10-02", "50", "expense", "", "Food")[0]


def test_edit_and_delete_and_isolation():
    a, b = make_user("user_a"), make_user("user_b")
    add_transaction(a["id"], "2026-10-02", "100", "expense", "Tea", "Food")
    txn_id = list_transactions(a["id"])[0]["id"]

    assert list_transactions(b["id"]) == []
    assert not update_transaction(b["id"], txn_id, "2026-10-02", "1", "expense", "Hack", "Food")[0]
    assert not delete_transaction(b["id"], txn_id)[0]
    assert len(list_transactions(a["id"])) == 1

    assert update_transaction(a["id"], txn_id, "2026-10-02", "200", "expense", "Tea", "Food")[0]
    assert list_transactions(a["id"])[0]["amount_paise"] == 20000
    assert delete_transaction(a["id"], txn_id)[0]
    assert list_transactions(a["id"]) == []


def test_budget_status():
    u = make_user()
    add_transaction(u["id"], "2026-10-10", "3500", "expense", "Meal", "Food")
    set_budget(u["id"], "2026-10", "Food", "4000")
    set_budget(u["id"], "2026-10", "Overall", "20000")
    result = {s["category"]: s for s in budget_status(u["id"], "2026-10")}
    assert result["Food"]["status"] == "warning"
    assert result["Food"]["percent_used"] == 87.5
    assert result["Overall"]["status"] == "ok"
    add_transaction(u["id"], "2026-10-11", "1000", "expense", "Meal2", "Food")
    result = {s["category"]: s for s in budget_status(u["id"], "2026-10")}
    assert result["Food"]["status"] == "exceeded"