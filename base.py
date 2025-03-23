import tkinter as tk
import sqlite3
from tkinter import ttk
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from datetime import datetime

root = tk.Tk()

root.geometry("950x600")
root.title("Expense Tracker")


# Create a database connection
connection = sqlite3.connect('expense_tracker.db')
cursor = connection.cursor()

# Create a table
def create_table():
    cursor.execute('''CREATE TABLE IF NOT EXISTS expenses (
                        Sl_No INTEGER PRIMARY KEY AUTOINCREMENT,
                        ITEM TEXT,
                        PRICE REAL,
                        DATE TEXT)''')
    connection.commit()

create_table()


# Add an item to the database
def add_item():
    item = item_entry.get()
    price = price_entry.get()
    date_today = datetime.now().strftime('%Y-%m-%d')

    cursor.execute('INSERT INTO expenses (ITEM, PRICE, DATE) VALUES (?, ?, ?)', (item, price, date_today))
    connection.commit()

    item_entry.delete(0, tk.END)
    price_entry.delete(0, tk.END)

    show_data()
    plot_graph()


# Fetch data from the database
def fetch_data(date_filter=None):
    if date_filter:
        cursor.execute('SELECT * FROM expenses WHERE DATE = ?', (date_filter,))
    else:
        cursor.execute('SELECT * FROM expenses')
    data = cursor.fetchall()
    return data


# Display data in the treeview
def show_data():
    date_filter = date_entry.get()
    data = fetch_data(date_filter)

    for row in tree.get_children():
        tree.delete(row)

    for i, row in enumerate(data):
        if i % 2 == 0:
            tree.insert("", tk.END, values=row, tags="even")
        else:
            tree.insert("", tk.END, values=row, tags="odd")

    tree.tag_configure("even", background="#f9f9f9")
    tree.tag_configure("odd", background="#e9e9e9")


# Calculate total expenses
def calculate_total():
    cursor.execute("SELECT SUM(PRICE) FROM expenses")
    total = cursor.fetchone()[0]
    if total is None:
        total = 0.0
    total_label.config(text=f"Total Expenses: ${total:.2f}")


# Plot a graph
def plot_graph():
    data = fetch_data()
    date_expenses = {}
    for row in data:
        date = row[3]
        price = row[2]
        if date in date_expenses:
            date_expenses[date] += price
        else:
            date_expenses[date] = price

    dates = list(date_expenses.keys())
    prices = list(date_expenses.values())

    fig, ax = plt.subplots(figsize=(5, 3))
    ax.bar(dates, prices, color="skyblue")
    ax.set_title("Total Price per Date")
    ax.set_xlabel("Date")
    ax.set_ylabel("Price ($)")

    for widget in frame3.winfo_children():
        widget.destroy()

    canvas = FigureCanvasTkAgg(fig, master=frame3)
    canvas.draw()
    canvas.get_tk_widget().grid(row=0, column=0, sticky="nsew")


# Close the database connection
def on_closing():
    connection.close()
    root.destroy()

root.protocol("WM_DELETE_WINDOW", on_closing)

#GUI ELEMENTS


frame1 = tk.Frame(root)
frame1.grid(row=1, column=0, sticky="nsew")
frame1.rowconfigure(1, weight=1)


item = tk.Label(frame1, text="Item")
item.grid(row=1, column=0)

item_entry = tk.Entry(frame1)
item_entry.grid(row=1, column=1)

price = tk.Label(frame1, text="Price")
price.grid(row=2, column=0)

price_entry = tk.Entry(frame1)
price_entry.grid(row=2, column=1)

date_label = tk.Label(frame1, text="Filter by Date (YYYY-MM-DD)")
date_label.grid(row=3, column=0, pady=10)

date_entry = tk.Entry(frame1)
date_entry.grid(row=3, column=1, pady=10)

filter_button = ttk.Button(frame1, text="Filter by Date", command=show_data)
filter_button.grid(row=3, column=2, padx=10)

frame2 = tk.Frame(root)
frame2.grid(row=2, column=0, sticky="nsew")

tree = ttk.Treeview(frame2, columns=("Sl_No", "Item", "Price", "Date"), show="headings")
tree.heading("Sl_No", text="Sl No.")
tree.heading("Item", text="Item")
tree.heading("Price", text="Price")
tree.heading("Date", text="Date")

tree.column("Sl_No", width=100, anchor=tk.CENTER)
tree.column("Item", width=200, anchor=tk.CENTER)
tree.column("Price", width=100, anchor=tk.CENTER)
tree.column("Date", width=120, anchor=tk.CENTER)

tree.grid(row=2, column=0, sticky="nsew")

header = tk.Label(root, text="Expense Tracker", font=("Arial", 24, "bold"))
header.grid(row=0, column=0, pady=10)

tree_scroll = tk.Scrollbar(frame2, orient="vertical", command=tree.yview)
tree_scroll.grid(row=0, column=1, sticky="ns")

tree.configure(yscrollcommand=tree_scroll.set)

show_data()

total_label = tk.Label(root, text="Total Expenses: $0.00", font=("Arial", 16, "bold"))
total_label.grid(row=3, column=0, pady=10)

footer = tk.Label(root, text="Version 1.0 - Use the form above to track your expenses.", font=("Arial", 10))
footer.grid(row=4, column=0, pady=10)

frame1.grid_rowconfigure(0, weight=1)
frame1.grid_columnconfigure(0, weight=1)
frame1.grid_columnconfigure(1, weight=2)
frame1.grid_columnconfigure(2, weight=1)

frame2.grid_rowconfigure(0, weight=1)
frame2.grid_columnconfigure(0, weight=1)

style = ttk.Style()
style.configure("TButton", font=("Arial", 12), padding=10)

submit = ttk.Button(frame1, text="Submit", command=add_item, style="TButton")
submit.grid(row=1, column=2, padx=10)

style.theme_use("clam")

frame1.grid_rowconfigure(1, weight=1)
frame1.grid_columnconfigure(0, weight=1)
frame1.grid_columnconfigure(1, weight=2)
frame1.grid_columnconfigure(2, weight=1)

frame2.grid_rowconfigure(0, weight=1)
frame2.grid_columnconfigure(0, weight=1)

tree.grid(row=0, column=0, sticky="nsew")

tree_scroll = tk.Scrollbar(frame2, orient="vertical", command=tree.yview)
tree_scroll.grid(row=0, column=1, sticky="ns")
tree.configure(yscrollcommand=tree_scroll.set)

header.grid(row=0, column=0, pady=10, padx=10, sticky="nsew", columnspan=3)

footer.grid(row=4, column=0, pady=10, padx=10, sticky="nsew", columnspan=3)

item_entry.grid(row=1, column=1, padx=5, pady=5, sticky="ew")
price_entry.grid(row=2, column=1, padx=5, pady=5, sticky="ew")

frame3 = tk.Frame(root)
frame3.grid(row=2, column=2, sticky="nsew", padx=10, pady=10)

plot_graph()

if __name__ == "__main__":
    root.mainloop()
