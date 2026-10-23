PRAGMA foreign_keys = ON;

CREATE TABLE IF NOT EXISTS users (
    id            INTEGER PRIMARY KEY AUTOINCREMENT,
    name          TEXT    NOT NULL,
    email         TEXT    NOT NULL UNIQUE,
    username      TEXT    NOT NULL UNIQUE,
    password_hash TEXT    NOT NULL,
    created_at    TEXT    NOT NULL DEFAULT (datetime('now'))
);

CREATE TABLE IF NOT EXISTS transactions (
    id               INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id          INTEGER NOT NULL,
    txn_date         TEXT    NOT NULL,
    amount_paise     INTEGER NOT NULL CHECK (amount_paise > 0),
    txn_type         TEXT    NOT NULL CHECK (txn_type IN ('income', 'expense')),
    description      TEXT    NOT NULL,
    category         TEXT    NOT NULL,
    payment_method   TEXT,
    notes            TEXT,
    created_at       TEXT    NOT NULL DEFAULT (datetime('now')),
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
);

CREATE INDEX IF NOT EXISTS idx_txn_user_date
    ON transactions (user_id, txn_date);

CREATE TABLE IF NOT EXISTS budgets (
    id           INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id      INTEGER NOT NULL,
    category     TEXT    NOT NULL,
    month        TEXT    NOT NULL,
    limit_paise  INTEGER NOT NULL CHECK (limit_paise > 0),
    created_at   TEXT    NOT NULL DEFAULT (datetime('now')),
    UNIQUE (user_id, category, month),
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
);

CREATE TABLE IF NOT EXISTS savings_goals (
    id                   INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id              INTEGER NOT NULL,
    goal_name            TEXT    NOT NULL,
    target_paise         INTEGER NOT NULL CHECK (target_paise > 0),
    saved_paise          INTEGER NOT NULL DEFAULT 0 CHECK (saved_paise >= 0),
    target_date          TEXT    NOT NULL,
    created_at           TEXT    NOT NULL DEFAULT (datetime('now')),
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
);