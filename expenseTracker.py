import os
import csv
from datetime import datetime
import tkinter as tk
from tkinter import messagebox, simpledialog

FILE_NAME = "expenses.csv"
VALID_MONTHS = ["JANUARY", "FEBRUARY", "MARCH", "APRIL", "MAY", "JUNE", "JULY", "AUGUST", "SEPTEMBER", "OCTOBER", "NOVEMBER", "DECEMBER"]

# Ensure the file exists and has headers
def initialize_file():
    if not os.path.exists(FILE_NAME):
        with open(FILE_NAME, 'w', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(["ID", "Month", "Year", "Type", "Concept", "Amount", "Day"])

# Function to get a valid month and year
def get_valid_month_and_year():
    while True:
        month = simpledialog.askstring("Input", "Enter month:")
        if month:
            month = month.strip().lower().capitalize()
            if month.upper() in VALID_MONTHS:
                year = simpledialog.askstring("Input", "Enter year:")
                if year and year.isdigit() and len(year) == 4:
                    return month.upper(), year
        messagebox.showerror("Error", "Invalid month or year. Please enter again.")

# Generate a sequential ID for a specific month and year
def get_next_id_for_month_year(month, year):
    try:
        with open(FILE_NAME, 'r') as file:
            reader = csv.reader(file)
            next(reader)
            ids = [int(row[0]) for row in reader if row[1] == month and row[2] == year]
        return max(ids) + 1 if ids else 1
    except FileNotFoundError:
        return 1

# Add a new expense
def add_expense():
    month, year = get_valid_month_and_year()
    concept = simpledialog.askstring("Input", "Expense concept:")
    amount = simpledialog.askstring("Input", "Amount:")
    day = simpledialog.askstring("Input", "Day:")
    expense_id = get_next_id_for_month_year(month, year)
    
    with open(FILE_NAME, 'a', newline='') as file:
        writer = csv.writer(file)
        writer.writerow([expense_id, month, year, "Expense", concept, amount, day])
    
    messagebox.showinfo("Success", "Expense added successfully!")

# Add a new income
def add_income():
    month, year = get_valid_month_and_year()
    concept = simpledialog.askstring("Input", "Income concept:")
    amount = simpledialog.askstring("Input", "Amount:")
    day = simpledialog.askstring("Input", "Day:")
    income_id = get_next_id_for_month_year(month, year)
    
    with open(FILE_NAME, 'a', newline='') as file:
        writer = csv.writer(file)
        writer.writerow([income_id, month, year, "Income", concept, amount, day])
    
    messagebox.showinfo("Success", "Income added successfully!")

# Calculate total expenses for a given month and year
def total_expenses(month, year):
    total = 0.0
    with open(FILE_NAME, 'r') as file:
        reader = csv.reader(file)
        next(reader)
        for row in reader:
            if row[1] == month and row[2] == year and row[3] == "Expense":
                total += float(row[5])
    return total

# Calculate total income for a given month and year
def total_income(month, year):
    total = 0.0
    with open(FILE_NAME, 'r') as file:
        reader = csv.reader(file)
        next(reader)
        for row in reader:
            if row[1] == month and row[2] == year and row[3] == "Income":
                total += float(row[5])
    return total

# Show balance
def show_balance():
    month, year = get_valid_month_and_year()
    balance = total_income(month, year) - total_expenses(month, year)
    messagebox.showinfo("Balance", f"Balance for {month} {year}: {balance}€")

# List all expenses
def list_expenses():
    month, year = get_valid_month_and_year()
    expenses = []
    with open(FILE_NAME, 'r') as file:
        reader = csv.reader(file)
        next(reader)
        for row in reader:
            if row[1] == month and row[2] == year and row[3] == "Expense":
                expenses.append(f"ID {row[0]} - {row[4]}: {row[5]}€ on day {row[6]}")
    if expenses:
        messagebox.showinfo("Expenses", "\n".join(expenses))
    else:
        messagebox.showinfo("Expenses", f"No expenses for {month} {year}.")

# Delete an expense
def delete_expense():
    month, year = get_valid_month_and_year()
    expenses = []
    with open(FILE_NAME, 'r') as file:
        reader = csv.reader(file)
        next(reader)
        for row in reader:
            if row[1] == month and row[2] == year and row[3] == "Expense":
                expenses.append(f"ID {row[0]} - {row[4]}: {row[5]}€ on day {row[6]}")
    if expenses:
        messagebox.showinfo("Expenses", "\n".join(expenses))
    else:
        messagebox.showinfo("Expenses", f"No expenses for {month} {year}.")
    expense_id = simpledialog.askstring("Input", "Enter the ID of the expense to delete:")
    rows = []
    deleted = False
    with open(FILE_NAME, 'r') as file:
        reader = csv.reader(file)
        rows = list(reader)
    with open(FILE_NAME, 'w', newline='') as file:
        writer = csv.writer(file)
        for row in rows:
            if row[0] == expense_id and row[1] == month and row[2] == year and row[3] == "Expense":
                deleted = True
                continue
            writer.writerow(row)
    if deleted:
        messagebox.showinfo("Success", "Expense deleted successfully!")
    else:
        messagebox.showerror("Error", "Expense not found.")

def show_total_expenses():
    month, year = get_valid_month_and_year()
    total = total_expenses(month, year)
    messagebox.showinfo("Total Expenses", f"Total expenses for {month} {year}: {total}€")

# Show total income
def show_total_income():
    month, year = get_valid_month_and_year()
    total = total_income(month, year)
    messagebox.showinfo("Total Income", f"Total income for {month} {year}: {total}€")



# Create the main UI
def open_ui():
    root = tk.Tk()
    root.title("Erasmus Expense Tracker")
    root.geometry("400x500")
    tk.Label(root, text="ERASMUS EXPENSE TRACKER", font=("Arial", 14)).pack(pady=10)
    tk.Button(root, text="Add New Expense", command=add_expense, width=30).pack(pady=5)
    tk.Button(root, text="Add New Income", command=add_income, width=30).pack(pady=5)
    tk.Button(root, text="Show Balance", command=show_balance, width=30).pack(pady=5)
    tk.Button(root, text="List All Expenses", command=list_expenses, width=30).pack(pady=5)
    tk.Button(root, text="Delete an Expense", command=delete_expense, width=30).pack(pady=5)
    tk.Button(root, text="Total Expenses", command=show_total_expenses, width=30).pack(pady=5)
    tk.Button(root, text="Total Income", command=show_total_income, width=30).pack(pady=5)
    tk.Button(root, text="Exit", command=root.quit, width=30).pack(pady=20)
    root.mainloop()

if __name__ == "__main__":
    initialize_file()
    open_ui()
