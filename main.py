import tkinter as tk
import json

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

        self.transactions_text = tk.Text(self, height=10, width=50)
        self.transactions_text.pack()

        # Create buttons for managing transactions
        self.add_button = tk.Button(self, text="Add Transaction", command=self.add_transaction)
        self.add_button.pack()
        self.view_button = tk.Button(self, text="View Transactions", command=self.view_transactions)
        self.view_button.pack()
        self.update_button = tk.Button(self, text="Update Transaction", command=self.update_transaction)
        self.update_button.pack()
        self.delete_button = tk.Button(self, text="Delete Transaction", command=self.delete_transaction)
        self.delete_button.pack()
        self.summary_button = tk.Button(self, text="Summary", command=self.display_summary)
        self.summary_button.pack()
        self.save_button = tk.Button(self, text="Save Data", command=self.save_data)
        self.save_button.pack()

    def load_data(self):
        try:
            with open('transactions.json', 'r') as file:
                self.transactions = json.load(file)
            self.update_transactions_display()
            print("Data loaded successfully.")
        except FileNotFoundError:
            print("No saved data found.")

    def search_transactions(self):
        search_date = self.search_entry.get().strip()
        filtered_transactions = [t for t in self.transactions if t['date'] == search_date]
        self.display_transactions(filtered_transactions)

    def update_transactions_display(self):
        self.transactions_text.delete('1.0', tk.END)
        for transaction in self.transactions:
            self.transactions_text.insert(tk.END, f"Date: {transaction['date']}, Description: {transaction['description']}, Amount: {transaction['amount']}, Category: {transaction['category']}\n")

    def display_transactions(self, transactions):
        self.transactions_text.delete('1.0', tk.END)
        for transaction in transactions:
            self.transactions_text.insert(tk.END, f"Date: {transaction['date']}, Description: {transaction['description']}, Amount: {transaction['amount']}, Category: {transaction['category']}\n")

    def add_transaction(self):
        date = self.search_entry.get().strip()
        description = input("Enter the description: ")  # Input via Tkinter not implemented here
        amount = float(input("Enter the amount: "))    # Input via Tkinter not implemented here
        category = input("Enter the category: ")        # Input via Tkinter not implemented here
        transaction_id = len(self.transactions) + 1
        transaction = {'id': transaction_id, 'date': date, 'description': description, 'amount': amount, 'category': category}
        self.transactions.append(transaction)
        self.update_transactions_display()
        print("Transaction added successfully.")

    def view_transactions(self):
        self.update_transactions_display()

    def update_transaction(self):
        transaction_id = int(input("Enter the transaction ID to update: "))  # Input via Tkinter not implemented here
        for transaction in self.transactions:
            if transaction['id'] == transaction_id:
                transaction['date'] = input("Enter the new date (YYYY-MM-DD): ")         # Input via Tkinter not implemented here
                transaction['description'] = input("Enter the new description: ")          # Input via Tkinter not implemented here
                transaction['amount'] = float(input("Enter the new amount: "))             # Input via Tkinter not implemented here
                transaction['category'] = input("Enter the new category: ")                    # Input via Tkinter not implemented here
                self.update_transactions_display()
                print("Transaction updated successfully.")
                return
        print("Transaction not found.")

    def delete_transaction(self):
        transaction_id = int(input("Enter the transaction ID to delete: "))   # Input via Tkinter not implemented here
        for i, transaction in enumerate(self.transactions):
            if transaction['id'] == transaction_id:
                del self.transactions[i]
                self.update_transactions_display()
                print("Transaction deleted successfully.")
                return
        print("Transaction not found.")

    def display_summary(self):
        total_income = sum(transaction['amount'] for transaction in self.transactions if transaction['amount'] > 0)
        total_expenses = sum(transaction['amount'] for transaction in self.transactions if transaction['amount'] < 0)
        net_balance = total_income + total_expenses
        print(f"\nSummary:")
        print(f"Total Income: {total_income}")
        print(f"Total Expenses: {total_expenses}")
        print(f"Net Balance: {net_balance}")

    def save_data(self):
        with open('transactions.json', 'w') as file:
            json.dump(self.transactions, file)
        print("Data saved successfully.")

if __name__ == "__main__":
    app = FinanceTrackerApp()
    app.mainloop()
