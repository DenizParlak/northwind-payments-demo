"""Database access helpers."""
import sqlite3

DB_PATH = "payments.db"


def get_connection():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn


def init_db():
    conn = get_connection()
    conn.executescript(
        """
        CREATE TABLE IF NOT EXISTS accounts (
            id INTEGER PRIMARY KEY,
            owner TEXT NOT NULL,
            balance INTEGER NOT NULL DEFAULT 0
        );
        CREATE TABLE IF NOT EXISTS transactions (
            id INTEGER PRIMARY KEY,
            account INTEGER NOT NULL,
            amount INTEGER NOT NULL,
            memo TEXT
        );
        """
    )
    conn.commit()
    conn.close()
