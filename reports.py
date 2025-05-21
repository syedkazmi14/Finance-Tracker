import matplotlib.pyplot as plt
from db import get_connection
import os
import pandas as pd

STATIC_DIR = "static/charts"

def get_summary():
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("SELECT SUM(amount) FROM transactions WHERE type='income'")
    income = cursor.fetchone()[0] or 0

    cursor.execute("SELECT SUM(amount) FROM transactions WHERE type='expense'")
    expenses = cursor.fetchone()[0] or 0

    conn.close()
    balance = income - expenses
    return {"income": income, "expenses": expenses, "balance": balance}

def save_income_vs_expense_chart():
    summary = get_summary()
    labels = ["Income", "Expenses"]
    values = [summary["income"], summary["expenses"]]

    plt.bar(labels, values, color=["green", "red"])
    plt.title("Income vs Expenses")
    plt.ylabel("Amount")
    os.makedirs(STATIC_DIR, exist_ok=True)
    plt.savefig(os.path.join(STATIC_DIR, "income_vs_expense.png"))
    plt.close()

def save_expenses_by_category_chart():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT category, SUM(amount) FROM transactions WHERE type='expense' GROUP BY category")
    data = cursor.fetchall()
    conn.close()

    if not data:
        return

    categories = [row[0] for row in data]
    amounts = [row[1] for row in data]

    plt.pie(amounts, labels=categories, autopct="%1.1f%%", startangle=90)
    plt.title("Expenses by Category")
    os.makedirs(STATIC_DIR, exist_ok=True)
    plt.savefig(os.path.join(STATIC_DIR, "expenses_by_category.png"))
    plt.close()

def save_monthly_trend_chart():
    conn = get_connection()
    df = None
    try:
        df = pd.read_sql_query("SELECT type, amount, date FROM transactions", conn)
    finally:
        conn.close()

    if df.empty:
        return

    df["date"] = pd.to_datetime(df["date"])
    df["month"] = df["date"].dt.to_period("M")

    summary = df.groupby(["month", "type"])["amount"].sum().unstack(fill_value=0)

    summary.plot(kind="line", marker="o")
    plt.title("Monthly Income and Expenses")
    plt.ylabel("Amount")
    plt.xlabel("Month")
    os.makedirs(STATIC_DIR, exist_ok=True)
    plt.savefig(os.path.join(STATIC_DIR, "monthly_trend.png"))
    plt.close()
