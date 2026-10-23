"""Shared pytest setup: every test runs against a fresh temporary database."""

import pytest

import database.db as db


@pytest.fixture(autouse=True)
def temp_database(tmp_path, monkeypatch):
    """Point the app at a throwaway SQLite file so real data is never touched."""
    monkeypatch.setattr(db, "DB_PATH", tmp_path / "test_finmate.db")
    db.init_db()
    yield