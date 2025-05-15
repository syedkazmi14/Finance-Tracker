import matplotlib.pyplot as plt
from db import get_connection

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


def plot_income_vs_expense():
    summary = get_summary()
    labels = ["Income", "Expenses"]
    values = [summary["income"], summary["expenses"]]

    plt.bar(labels, values)
    plt.title("Income vs Expenses")
    plt.ylabel("Amount")
    plt.show()


def plot_expenses_by_category():
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("SELECT category, SUM(amount) FROM transactions WHERE type='expense' GROUP BY category")
    data = cursor.fetchall()
    conn.close()

    if not data:
        print("No expenses recorded yet.")
        return

    categories = [row[0] for row in data]
    amounts = [row[1] for row in data]

    plt.pie(amounts, labels=categories, autopct="%1.1f%%", startangle=90)
    plt.title("Expenses by Category")
    plt.show()
