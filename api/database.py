import sqlite3
import os

DB_PATH = "genxdb_fx.db"


def init_db():
    """Initializes the database with required tables."""
    db = sqlite3.connect(DB_PATH, check_same_thread=False)
    cursor = db.cursor()

    # Create users table
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY,
        username TEXT NOT NULL UNIQUE,
        email TEXT NOT NULL UNIQUE,
        is_active INTEGER DEFAULT 1
    )
    """)

    # Create trading_pairs table
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS trading_pairs (
        id INTEGER PRIMARY KEY,
        symbol TEXT NOT NULL UNIQUE,
        base_currency TEXT NOT NULL,
        quote_currency TEXT NOT NULL,
        is_active INTEGER DEFAULT 1
    )
    """)

    # Create payment_methods table
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS payment_methods (
        id INTEGER PRIMARY KEY,
        cardholder_name TEXT,
        masked_card_number TEXT
    )
    """)

    # Create account_performance table
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS account_performance (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        account_number TEXT NOT NULL,
        balance REAL,
        equity REAL,
        total_profit REAL,
        total_loss REAL,
        pnl REAL,
        profit_factor REAL,
        currency TEXT DEFAULT 'USD',
        timestamp TEXT
    )
    """)

    db.commit()
    db.close()


# Initialize database on module load
init_db()


def get_db():
    """
    FastAPI dependency to get a database connection for each request.
    """
    db = sqlite3.connect(DB_PATH, check_same_thread=False)
    db.row_factory = sqlite3.Row
    try:
        yield db
    finally:
        db.close()
