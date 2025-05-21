from db import get_connection

def add_transaction(type, category, amount, date, description=""):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO transactions (type, category, amount, date, description)
        VALUES (?, ?, ?, ?, ?)
    """, (type, category, amount, date, description))
    conn.commit()
    conn.close()

def get_all_transactions():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM transactions ORDER BY date DESC")
    rows = cursor.fetchall()
    conn.close()
    return rows

def delete_transaction(transaction_id):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM transactions WHERE id = ?", (transaction_id,))
    conn.commit()
    conn.close()

def filter_transactions(category="", start_date=None, end_date=None):
    conn = get_connection()
    cursor = conn.cursor()

    query = "SELECT * FROM transactions WHERE 1=1"
    params = []

    if category:
        query += " AND category LIKE ?"
        params.append(f"%{category}%")

    if start_date:
        query += " AND date >= ?"
        params.append(start_date)

    if end_date:
        query += " AND date <= ?"
        params.append(end_date)

    query += " ORDER BY date DESC"
    cursor.execute(query, tuple(params))
    rows = cursor.fetchall()
    conn.close()
    return rows
