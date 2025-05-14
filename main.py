from models import add_transaction, get_all_transactions
from reports import get_summary
from db import create_tables
from utils import validate_date

def main_menu():
    create_tables()
    while True:
        print("\n--- Personal Finance Manager ---")
        print("1. Add Transaction")
        print("2. View All Transactions")
        print("3. View Summary")
        print("4. Exit")

        choice = input("Choose an option: ")

        if choice == "1":
            type = input("Type (income/expense): ").lower()
            category = input("Category: ")
            amount = float(input("Amount: "))
            date = input("Date (YYYY-MM-DD): ")

            if not validate_date(date):
                print("Invalid date format.")
                continue

            description = input("Description (optional): ")
            add_transaction(type, category, amount, date, description)
            print("Transaction added.")

        elif choice == "2":
            transactions = get_all_transactions()
            for t in transactions:
                print(t)

        elif choice == "3":
            summary = get_summary()
            print(f"Total Income: {summary['income']}")
            print(f"Total Expenses: {summary['expenses']}")
            print(f"Balance: {summary['balance']}")

        elif choice == "4":
            print("Exiting...")
            break
        else:
            print("Invalid choice.")

if __name__ == "__main__":
    main_menu()
