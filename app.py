from flask import Flask, render_template, request, redirect, url_for, flash
from db import create_tables
from models import add_transaction, get_all_transactions, delete_transaction, filter_transactions
from reports import get_summary, save_income_vs_expense_chart, save_expenses_by_category_chart, save_monthly_trend_chart
from utils import validate_date

app = Flask(__name__)
app.secret_key = "supersecretkey"  # needed for flash messages

@app.route("/")
def home():
    summary = get_summary()
    transactions = get_all_transactions()
    return render_template("index.html", summary=summary, transactions=transactions)

@app.route("/add", methods=["GET", "POST"])
def add():
    if request.method == "POST":
        type = request.form["type"].lower()
        category = request.form["category"].strip()
        amount = request.form["amount"]
        date = request.form["date"]
        description = request.form.get("description", "").strip()

        # Validation
        if not amount or float(amount) <= 0:
            flash("Amount must be greater than 0.", "danger")
            return redirect(url_for("add"))
        if not validate_date(date):
            flash("Invalid date format. Use YYYY-MM-DD.", "danger")
            return redirect(url_for("add"))

        add_transaction(type, category, float(amount), date, description)
        flash("Transaction added successfully!", "success")
        return redirect(url_for("home"))

    return render_template("add.html")

@app.route("/delete/<int:transaction_id>")
def delete(transaction_id):
    delete_transaction(transaction_id)
    flash("Transaction deleted successfully.", "info")
    return redirect(url_for("home"))

@app.route("/charts")
def charts():
    save_income_vs_expense_chart()
    save_expenses_by_category_chart()
    save_monthly_trend_chart()
    return render_template("chart.html")

@app.route("/filter", methods=["GET", "POST"])
def filter_page():
    results = []
    if request.method == "POST":
        category = request.form.get("category", "").strip()
        start_date = request.form.get("start_date")
        end_date = request.form.get("end_date")
        results = filter_transactions(category, start_date, end_date)
    return render_template("filter.html", results=results)

if __name__ == "__main__":
    create_tables()
    app.run(debug=True)
