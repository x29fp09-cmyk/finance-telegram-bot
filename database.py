import sqlite3
from datetime import datetime

conn = sqlite3.connect("finance.db", check_same_thread=False)
cursor = conn.cursor()

def init_db():
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS expenses (
        id INTEGER PRIMARY KEY,
        amount INTEGER,
        category TEXT,
        date TEXT
    )
    """)

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS incomes (
        id INTEGER PRIMARY KEY,
        amount INTEGER,
        date TEXT
    )
    """)
    conn.commit()

def add_expense(amount, category):
    cursor.execute(
        "INSERT INTO expenses (amount, category, date) VALUES (?, ?, ?)",
        (amount, category, datetime.now().strftime("%Y-%m-%d"))
    )
    conn.commit()

def add_income(amount):
    cursor.execute(
        "INSERT INTO incomes (amount, date) VALUES (?, ?)",
        (amount, datetime.now().strftime("%Y-%m-%d"))
    )
    conn.commit()

def get_totals():
    cursor.execute("SELECT COALESCE(SUM(amount), 0) FROM expenses")
    total_expenses = cursor.fetchone()[0]

    cursor.execute("SELECT COALESCE(SUM(amount), 0) FROM incomes")
    total_incomes = cursor.fetchone()[0]

    balance = total_incomes - total_expenses
    return total_incomes, total_expenses, balance