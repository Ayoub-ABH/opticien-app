import tkinter as tk
from tkinter import ttk
import sqlite3
import tkinter.messagebox

# Setup SQLite database
conn = sqlite3.connect("optician_clients.db")
cursor = conn.cursor()

# Create a table to store client data if not exists
cursor.execute('''
    CREATE TABLE IF NOT EXISTS clients (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT,
        date TEXT,
        doctor TEXT,
        od_power REAL,
        og_power REAL,
        add_power REAL,
        glass_type TEXT,
        company TEXT,
        price REAL
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
    paginate_data()  # Refresh table data after saving new client

# Function to delete a selected client
def delete_client():
    selected_item = tree.selection()
    if selected_item:
        client_id = tree.item(selected_item)['values'][0]  # Get the ID of the selected client
        cursor.execute("DELETE FROM clients WHERE id=?", (client_id,))
        conn.commit()
        paginate_data()  # Reload the table data
    else:
        tk.messagebox.showwarning("Sélectionner un client", "Veuillez sélectionner un client à supprimer.")


def search_client():
    search_term = search_entry.get().lower()
    query = f"SELECT * FROM clients WHERE lower(date) LIKE ? OR lower(doctor) LIKE ?"
    cursor.execute(query, ('%' + search_term + '%', '%' + search_term + '%'))
    results = cursor.fetchall()
    update_table(results)  # Update the table with the search results


# Function to update the table view
def update_table(data):
    tree.delete(*tree.get_children())  # Clear the current table
    for row in data:
        tree.insert("", "end", values=row)
    # Recalculate total pages for pagination
    global total_pages
    total_pages = max(1, (len(data) + rows_per_page - 1) // rows_per_page)
    pagination_label.config(text=f"Page {current_page} sur {total_pages}")
    paginate_data()

# Function for adding a client (opens a popup form)
def open_add_client_window(parent):
    add_window = tk.Toplevel(parent)
    add_window.title("Ajouter un nouveau client")

    labels = ["N/P", "Date", "Docteur", "OD Puissance", "OG Puissance", "ADD Puissance", "Nature verre", "Société", "Prix"]
    entries = {}

    for i, label in enumerate(labels):
        tk.Label(add_window, text=label).grid(row=i, column=0, padx=10, pady=5)
        entry = ttk.Entry(add_window)
        entry.grid(row=i, column=1, padx=10, pady=5)
        entries[label] = entry

    # Function to submit client data
    def submit_client():
        client_data = [entries[label].get() for label in labels]
        save_data(client_data)  # Save data to the database
        add_window.destroy()  # Close the popup window

    submit_button = ttk.Button(add_window, text="Ajouter", command=submit_client)
    submit_button.grid(row=len(labels), column=0, columnspan=2, pady=10)

    add_window.transient(parent)
    add_window.grab_set()
    parent.wait_window(add_window)

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
    def search_client():
    global search_term
    search_term = search_entry.get().lower()
    query = f"SELECT * FROM clients WHERE lower(date) LIKE ? OR lower(doctor) LIKE ?"
    cursor.execute(query, ('%' + search_term + '%', '%' + search_term + '%'))
    results = cursor.fetchall()
    update_table(results)

# Set up the main window
root = tk.Tk()
root.title("Tableau des informations")
root.configure(bg="#f0f0f0")

# Frame for buttons and search
button_frame = ttk.Frame(root, padding="10")
button_frame.grid(row=0, column=0, padx=10, pady=10, sticky="ew")

add_button = ttk.Button(button_frame, text="Ajouter Client", command=lambda: open_add_client_window(root))
add_button.grid(row=0, column=0, padx=10)

search_entry = ttk.Entry(button_frame, width=80)
search_entry.grid(row=0, column=1, padx=10)

search_button = ttk.Button(button_frame, text="Rechercher", command=search_client)
search_button.grid(row=0, column=2, padx=10)

# Button to delete selected client
delete_button = ttk.Button(button_frame, text="Supprimer Client", command=delete_client)
delete_button.grid(row=0, column=3, padx=10)

# Treeview for displaying client data
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
rows_per_page = 10
current_page = 1
data = load_data()
total_pages = max(1, (len(data) + rows_per_page - 1) // rows_per_page)

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

# Start with initial data
paginate_data()

root.mainloop()
