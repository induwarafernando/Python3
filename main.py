import tkinter as tk
import json
from tkinter import ttk

class FinanceTrackerApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Finance Tracker")
        self.transactions = []  # Initialize transactions list

        # Load data from JSON file
        self.load_data()

        # Create and pack widgets
        self.label = tk.Label(self, text="Welcome to Finance Tracker")
        self.label.pack()

        self.search_label = tk.Label(self, text="Search by Date (YYYY-MM-DD):")
        self.search_label.pack()
        self.search_entry = tk.Entry(self)
        self.search_entry.pack()
        self.search_button = tk.Button(self, text="Search", command=self.search_transactions)
        self.search_button.pack()

        # Create buttons for managing transactions
        self.add_button = tk.Button(self, text="Add Transaction", command=self.add_transaction_window)
        self.add_button.pack()
        self.view_button = tk.Button(self, text="View Transactions", command=self.view_transactions)
        self.view_button.pack()
        self.update_button = tk.Button(self, text="Update Transaction", command=self.update_transaction_window)
        self.update_button.pack()
        self.delete_button = tk.Button(self, text="Delete Transaction", command=self.delete_transaction_window)
        self.delete_button.pack()
        self.summary_button = tk.Button(self, text="Summary", command=self.display_summary_window)
        self.summary_button.pack()
        self.save_button = tk.Button(self, text="Save Data", command=self.save_data)
        self.save_button.pack()

    def load_data(self):
        try:
            with open('transactions.json', 'r') as file:
                self.transactions = json.load(file)
        except FileNotFoundError:
            pass

    def search_transactions(self):
        search_date = self.search_entry.get().strip()
        if search_date:
            filtered_transactions = [t for t in self.transactions if t['date'] == search_date]
            self.display_transactions(filtered_transactions)
        else:
            self.display_transactions()

    def display_transactions(self, transactions=None):
        if transactions is None:
            transactions = self.transactions

        # Create a new window for displaying transactions
        self.transactions_window = tk.Toplevel(self)
        self.transactions_window.title("View Transactions")

        # Create a treeview to display transactions
        tree = ttk.Treeview(self.transactions_window, columns=("Date", "Description", "Amount", "Category"))
        tree.heading("#0", text="ID")
        tree.heading("Date", text="Date")
        tree.heading("Description", text="Description")
        tree.heading("Amount", text="Amount")
        tree.heading("Category", text="Category")

        for transaction in transactions:
            tree.insert("", "end", text=transaction['id'], values=(transaction['date'], transaction['description'], transaction['amount'], transaction['category']))

        tree.pack()

    def add_transaction_window(self):
        # Create a new window for adding transaction
        self.add_window = tk.Toplevel()
        self.add_window.title("Add Transaction")

        # Create and pack widgets for adding transaction
        tk.Label(self.add_window, text="Date (YYYY-MM-DD):").pack()
        self.date_entry = tk.Entry(self.add_window)
        self.date_entry.pack()

        tk.Label(self.add_window, text="Description:").pack()
        self.description_entry = tk.Entry(self.add_window)
        self.description_entry.pack()

        tk.Label(self.add_window, text="Amount:").pack()
        self.amount_entry = tk.Entry(self.add_window)
        self.amount_entry.pack()

        tk.Label(self.add_window, text="Category:").pack()
        self.category_entry = tk.Entry(self.add_window)
        self.category_entry.pack()

        tk.Button(self.add_window, text="Add", command=self.add_transaction).pack()

    def add_transaction(self):
        date = self.date_entry.get().strip()
        description = self.description_entry.get().strip()
        amount = float(self.amount_entry.get().strip())
        category = self.category_entry.get().strip()
        transaction_id = len(self.transactions) + 1
        transaction = {'id': transaction_id, 'date': date, 'description': description, 'amount': amount, 'category': category}
        self.transactions.append(transaction)
        self.add_window.destroy()  # Close the add window after adding the transaction
        self.save_data()  # Save the data after adding transaction
        self.search_transactions()  # Update the displayed transactions

    def view_transactions(self):
        self.display_transactions()

    def update_transaction_window(self):
        # Create a new window for updating transaction
        self.update_window = tk.Toplevel()
        self.update_window.title("Update Transaction")

        # Create and pack widgets for updating transaction
        tk.Label(self.update_window, text="Transaction ID to update:").pack()
        self.transaction_id_entry = tk.Entry(self.update_window)
        self.transaction_id_entry.pack()

        tk.Button(self.update_window, text="Update", command=self.update_transaction_data_window).pack()

    def update_transaction_data_window(self):
        transaction_id = int(self.transaction_id_entry.get().strip())
        transaction = self.get_transaction_by_id(transaction_id)
        if transaction:
            self.update_window.destroy()
            self.update_transaction_data(transaction)
        else:
            print("Transaction not found.")

    def update_transaction_data(self, transaction):
        # Create a new window for updating transaction data
        self.update_data_window = tk.Toplevel()
        self.update_data_window.title("Update Transaction Data")

        # Populate entry fields with existing data
        tk.Label(self.update_data_window, text="Date (YYYY-MM-DD):").pack()
        self.date_entry = tk.Entry(self.update_data_window)
        self.date_entry.insert(0, transaction['date'])
        self.date_entry.pack()

        tk.Label(self.update_data_window, text="Description:").pack()
        self.description_entry = tk.Entry(self.update_data_window)
        self.description_entry.insert(0, transaction['description'])
        self.description_entry.pack()

        tk.Label(self.update_data_window, text="Amount:").pack()
        self.amount_entry = tk.Entry(self.update_data_window)
        self.amount_entry.insert(0, transaction['amount'])
        self.amount_entry.pack()

        tk.Label(self.update_data_window, text="Category:").pack()
        self.category_entry = tk.Entry(self.update_data_window)
        self.category_entry.insert(0, transaction['category'])
        self.category_entry.pack()

        tk.Button(self.update_data_window, text="Update", command=lambda: self.update_transaction_data_confirm(transaction)).pack()

    def update_transaction_data_confirm(self, transaction):
        # Update transaction data
        transaction['date'] = self.date_entry.get().strip()
        transaction['description'] = self.description_entry.get().strip()
        transaction['amount'] = float(self.amount_entry.get().strip())
        transaction['category'] = self.category_entry.get().strip()

        # Update displayed transactions
        self.search_transactions()
        self.update_data_window.destroy()  # Close the update data window after updating the transaction data

    def delete_transaction_window(self):
        # Create a new window for deleting transaction
        self.delete_window = tk.Toplevel()
        self.delete_window.title("Delete Transaction")

        # Create and pack widgets for deleting transaction
        tk.Label(self.delete_window, text="Transaction ID to delete:").pack()
        self.delete_id_entry = tk.Entry(self.delete_window)
        self.delete_id_entry.pack()

        tk.Button(self.delete_window, text="Delete", command=self.delete_transaction).pack()

    def delete_transaction(self):
        transaction_id = int(self.delete_id_entry.get().strip())
        for i, transaction in enumerate(self.transactions):
            if transaction['id'] == transaction_id:
                del self.transactions[i]
                self.delete_window.destroy()  # Close the delete window after deleting the transaction
                self.save_data()  # Save the data after deleting transaction
                self.search_transactions()  # Update the displayed transactions
                return
        print("Transaction not found.")

    def display_summary_window(self):
        # Create a new window for displaying summary
        self.summary_window = tk.Toplevel()
        self.summary_window.title("Summary")

        # Calculate summary
        total_income = sum(transaction['amount'] for transaction in self.transactions if transaction['amount'] > 0)
        total_expenses = sum(transaction['amount'] for transaction in self.transactions if transaction['amount'] < 0)
        net_balance = total_income + total_expenses

        # Display summary
        tk.Label(self.summary_window, text=f"Total Income: {total_income}").pack()
        tk.Label(self.summary_window, text=f"Total Expenses: {total_expenses}").pack()
        tk.Label(self.summary_window, text=f"Net Balance: {net_balance}").pack()

    def save_data(self):
        with open('transactions.json', 'w') as file:
            json.dump(self.transactions, file)
        print("Data saved successfully.")

    def get_transaction_by_id(self, transaction_id):
        for transaction in self.transactions:
            if transaction['id'] == transaction_id:
                return transaction
        return None

if __name__ == "__main__":
    app = FinanceTrackerApp()
    app.mainloop()
