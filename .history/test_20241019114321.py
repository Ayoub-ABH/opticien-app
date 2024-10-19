import tkinter as tk
from tkinter import ttk
import sqlite3

# Setup SQLite database
conn = sqlite3.connect("optician_clients.db")
cursor = conn.cursor()

# Create a table to store client data
cursor.execute('''
    CREATE TABLE IF NOT EXISTS clients (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT,
        date TEXT,
        doctor TEXT,
        od_power TEXT,
        og_power TEXT,
        add_power TEXT,
        glass_type TEXT,
        company TEXT,
        price TEXT
                 CREATE TABLE IF NOT EXISTS clients (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT,             -- Name of the client
        date TEXT,             -- Date as a string (can be changed to a proper date type)
        doctor TEXT,           -- Name of the doctor
        od_power REAL,         -- OD power (number)
        og_power REAL,         -- OG power (number)
        add_power REAL,        -- ADD power (number)
        glass_type TEXT,       -- Type of glass
        company TEXT,          -- Company name
        price REAL             -- Price (number)
    )
    )
''')
conn.commit()

# Function to load data from SQLite
def load_data():
    cursor.execute("SELECT * FROM clients")
    return cursor.fetchall()

# Function to save a new client in SQLite
def save_data(new_client):
    cursor.execute('''
        INSERT INTO clients (name, date, doctor, od_power, og_power, add_power, glass_type, company, price)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
    ''', new_client)
    conn.commit()

# Function to search for clients by date or doctor
def search_client():
    search_term = search_entry.get().lower()
    query = f"SELECT * FROM clients WHERE lower(date) LIKE ? OR lower(doctor) LIKE ?"
    cursor.execute(query, ('%' + search_term + '%', '%' + search_term + '%'))
    results = cursor.fetchall()
    # Clear the current table
    tree.delete(*tree.get_children())
    # Insert search results into the treeview
    for row in results:
        tree.insert("", "end", values=row)

# Function to add a client (with an input form)
def add_client():
    def add_client_callback():
        new_client = (
            name_entry.get(),
            date_entry.get(),
            doctor_entry.get(),
            od_entry.get(),
            og_entry.get(),
            add_entry.get(),
            glass_type_entry.get(),
            company_entry.get(),
            price_entry.get(),
        )
        save_data(new_client)
        paginate_data()

        add_window.destroy()

    # Open a new window to input client data
    add_window = tk.Toplevel(root)
    add_window.title("Ajouter Client")

    tk.Label(add_window, text="Nom Prénom:").grid(row=0, column=0)
    tk.Label(add_window, text="Date:").grid(row=1, column=0)
    tk.Label(add_window, text="Docteur:").grid(row=2, column=0)
    tk.Label(add_window, text="OD Puissance:").grid(row=3, column=0)
    tk.Label(add_window, text="OG Puissance:").grid(row=4, column=0)
    tk.Label(add_window, text="ADD Puissance:").grid(row=5, column=0)
    tk.Label(add_window, text="Nature Verre:").grid(row=6, column=0)
    tk.Label(add_window, text="Société:").grid(row=7, column=0)
    tk.Label(add_window, text="Prix:").grid(row=8, column=0)

    name_entry = tk.Entry(add_window)
    date_entry = tk.Entry(add_window)
    doctor_entry = tk.Entry(add_window)
    od_entry = tk.Entry(add_window)
    og_entry = tk.Entry(add_window)
    add_entry = tk.Entry(add_window)
    glass_type_entry = tk.Entry(add_window)
    company_entry = tk.Entry(add_window)
    price_entry = tk.Entry(add_window)

    name_entry.grid(row=0, column=1)
    date_entry.grid(row=1, column=1)
    doctor_entry.grid(row=2, column=1)
    od_entry.grid(row=3, column=1)
    og_entry.grid(row=4, column=1)
    add_entry.grid(row=5, column=1)
    glass_type_entry.grid(row=6, column=1)
    company_entry.grid(row=7, column=1)
    price_entry.grid(row=8, column=1)

    add_button = tk.Button(add_window, text="Ajouter", command=add_client_callback)
    add_button.grid(row=9, column=0, columnspan=2)

# Function for pagination
def paginate_data():
    tree.delete(*tree.get_children())
    data = load_data()

    # Paginate and display the data
    start = (current_page - 1) * rows_per_page
    end = min(start + rows_per_page, len(data))
    
    for row in data[start:end]:
        tree.insert("", "end", values=row)
    
    pagination_label.config(text=f"Page {current_page} sur {total_pages}")

# Set up the main window
root = tk.Tk()
root.title("Tableau des informations")
root.configure(bg="#f0f0f0")

# Create a frame for buttons and search
button_frame = ttk.Frame(root, padding="10")
button_frame.grid(row=0, column=0, padx=10, pady=10, sticky="ew")

add_button = ttk.Button(button_frame, text="Ajouter Client", command=add_client)
add_button.grid(row=0, column=0, padx=10)

search_entry = ttk.Entry(button_frame, width=30)
search_entry.grid(row=0, column=1, padx=10)

search_button = ttk.Button(button_frame, text="Rechercher", command=search_client)
search_button.grid(row=0, column=2, padx=10)

# Create the Treeview (table)
columns = ("ID", "N/P", "Date", "Docteur", "OD Puissance", "OG Puissance", "ADD Puissance", "Nature Verre", "Société", "Prix")
tree = ttk.Treeview(root, columns=columns, show="headings")

for col in columns:
    tree.heading(col, text=col)

tree.grid(row=1, column=0, padx=10, pady=10, sticky="nsew")

# Pagination controls
pagination_frame = ttk.Frame(root, padding="10")
pagination_frame.grid(row=2, column=0, padx=10, pady=10, sticky="ew")

prev_button = ttk.Button(pagination_frame, text="Précédent", command=lambda: prev_page())
prev_button.grid(row=0, column=0, padx=10)

pagination_label = ttk.Label(pagination_frame, text=f"Page 1 sur 1")
pagination_label.grid(row=0, column=1)

next_button = ttk.Button(pagination_frame, text="Suivant", command=lambda: next_page())
next_button.grid(row=0, column=2, padx=10)

# Initial pagination setup
rows_per_page = 5
current_page = 1
data = load_data()
total_pages = max(1, (len(data) + rows_per_page - 1) // rows_per_page)

paginate_data()

# Functions to handle pagination
def prev_page():
    global current_page
    if current_page > 1:
        current_page -= 1
        paginate_data()

def next_page():
    global current_page
    if current_page < total_pages:
        current_page += 1
        paginate_data()

root.mainloop()
