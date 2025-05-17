from flask import Flask, render_template, request, redirect, url_for
from db import create_tables
from models import add_transaction, get_all_transactions
from reports import get_summary, save_income_vs_expense_chart, save_expenses_by_category_chart

app = Flask(__name__)

@app.route("/")
def home():
    summary = get_summary()
    transactions = get_all_transactions()
    return render_template("index.html", summary=summary, transactions=transactions)

@app.route("/add", methods=["POST"])
def add():
    type = request.form["type"].lower()
    category = request.form["category"]
    amount = float(request.form["amount"])
    date = request.form["date"]
    description = request.form.get("description", "")

    add_transaction(type, category, amount, date, description)
    return redirect(url_for("home"))

@app.route("/charts")
def charts():
    save_income_vs_expense_chart()
    save_expenses_by_category_chart()
    return render_template("chart.html")

if __name__ == "__main__":
    create_tables()
    app.run(debug=True)
