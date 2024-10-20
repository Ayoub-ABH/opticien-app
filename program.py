import tkinter as tk
from tkinter import ttk, filedialog
import sqlite3
import pandas as pd
import tkinter.messagebox
from PIL import Image, ImageTk

# Setup SQLite database
conn = sqlite3.connect("assets/optician_clients.db")
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

# Function to update a selected client data with a pupup window
def update_client():
    selected_item = tree.selection()
    if selected_item:
        client_id = tree.item(selected_item)['values'][0]  # Get the ID of the selected client
        client_data = tree.item(selected_item)['values'][1:]  # Get the data of the selected client
        
        update_window = tk.Toplevel(root)
        update_window.title("Modifier les informations du client")
        
        labels = ["N/P", "Date", "Docteur", "OD Puissance", "OG Puissance", "ADD Puissance", "Nature verre", "Société", "Prix"]
        entries = {}
        
        for i, label in enumerate(labels):
            tk.Label(update_window, text=label).grid(row=i, column=0, padx=50, pady=5)
            entry = ttk.Entry(update_window)
            entry.insert(0, client_data[i])  # Insert the current data into the entry field
            entry.grid(row=i, column=1, padx=50, pady=10)
            entries[label] = entry
        
        # Function to submit updated client data
        def submit_update():
            updated_data = [entries[label].get() for label in labels]
            cursor.execute(''' 
                UPDATE clients SET name=?, date=?, doctor=?, od_power=?, og_power=?, add_power=?, glass_type=?, company=?, price=? 
                WHERE id=?
            ''', (*updated_data, client_id))
            conn.commit()
            update_window.destroy()  # Close the popup window
            paginate_data()  # Reload the table data
        
        submit_button = ttk.Button(update_window, text="Modifier", command=submit_update, style="Red.TButton")
        submit_button.grid(row=len(labels), column=0, columnspan=2, pady=10)
    else:
        tk.messagebox.showwarning("Sélectionner un client", "Veuillez sélectionner un client à modifier.")


# Global variable to store search results
search_results = None

# Function to search for clients
def search_client():
    global search_results, current_page, total_pages
    search_term = search_entry.get().lower()
    
    # Query to search by name, date, or doctor
    query = f"""
        SELECT * FROM clients 
        WHERE lower(name) LIKE ? 
        OR lower(date) LIKE ? 
        OR lower(doctor) LIKE ? 
    """
    cursor.execute(query, ('%' + search_term + '%', '%' + search_term + '%', '%' + search_term + '%'))
    
    search_results = cursor.fetchall()
    
    # Check if no results were found
    if not search_results:
        tk.messagebox.showinfo("Aucun Résultat", "Aucun client ne correspond à votre recherche.")
    
    current_page = 1  # Reset to the first page on search
    total_pages = max(1, (len(search_results) + rows_per_page - 1) // rows_per_page)  # Recalculate total pages based on search results
    paginate_data()  # Update table with search results

# Function to clear the search and reset to full data
def clear_search():
    global search_results, current_page, total_pages
    search_entry.delete(0, tk.END)  # Clear the search input
    search_results = None  # Reset search results
    current_page = 1  # Reset to the first page
    total_pages = (len(load_data()) + rows_per_page - 1) // rows_per_page  # Recalculate total pages for full data
    paginate_data()  # Refresh table to show full data

# Function to update the table view
def update_table(data):
    tree.delete(*tree.get_children())  # Clear the current table
    for row in data:
        tree.insert("", "end", values=row)
    pagination_label.config(text=f"Page {current_page} sur {total_pages}")

# Function for pagination
def paginate_data():
    tree.delete(*tree.get_children())
    data = search_results if search_results else load_data()  # Use search results if available
    
    # Paginate and display the data
    start = (current_page - 1) * rows_per_page
    end = min(start + rows_per_page, len(data))
    
    for index, row in enumerate(data[start:end]):
        tag = 'even' if index % 2 == 0 else 'odd'  # Determine tag based on index
        tree.insert("", tk.END, values=row, tags=(tag,))  # Insert row with tag
    
    pagination_label.config(text=f"Page {current_page} sur {total_pages}")

def open_add_client_window(parent):
    add_window = tk.Toplevel(parent)
    add_window.title("Ajouter un nouveau client")
    
    labels = ["N/P", "Date", "Docteur", "OD Puissance", "OG Puissance", "ADD Puissance", "Nature verre", "Société", "Prix"]
    entries = {}

    for i, label in enumerate(labels):
        tk.Label(add_window, text=label).grid(row=i, column=0, padx=50, pady=5)
        entry = ttk.Entry(add_window)
        entry.grid(row=i, column=1, padx=50, pady=10)
        entries[label] = entry

    # Function to submit client data
    def submit_client():
        client_data = [entries[label].get() for label in labels]
        save_data(client_data)  # Save data to the database
        add_window.destroy()  # Close the popup window

    submit_button = ttk.Button(add_window, text="Ajouter", command=submit_client , style="Red.TButton")
    submit_button.grid(row=len(labels), column=0, columnspan=2, pady=10)

    add_window.transient(parent)
    add_window.grab_set()
    parent.wait_window(add_window)

# Function for next page
def next_page():
    global current_page
    if current_page < total_pages:
        current_page += 1
        paginate_data()

# Function for previous page
def prev_page():
    global current_page
    if current_page > 1:
        current_page -= 1
        paginate_data()

# Function to import data from an Excel file
def import_excel():
    file_path = filedialog.askopenfilename(filetypes=[("Excel Files", "*.xlsx")])
    if not file_path:
        return
    
    try:
        # Load the Excel file
        df = pd.read_excel(file_path)
        
        # Insert data from the Excel file into the database
        for _, row in df.iterrows():
            new_client = (row['name'], row['date'], row['doctor'], row['od_power'], row['og_power'], row['add_power'], row['glass_type'], row['company'], row['price'])
            save_data(new_client)
        
        tk.messagebox.showinfo("Succès", "Clients importés avec succès !")
    except Exception as e:
        tk.messagebox.showerror("Erreur", f"Erreur lors de l'importation : {e}")


# Set up the main window
root = tk.Tk()
root.title("Tableau des informations sur les clients")

# set the window icon
root.iconbitmap("assets/logo.ico")

# Load the logo
image = Image.open("assets/logo.jpg")
image = image.resize((50, 50))  # Replace with your image path
logo = ImageTk.PhotoImage(image)

# Create a label for the logo and add the image to it
logo_label = tk.Label(root, image=logo)
logo_label.grid(row=0, column=0, padx=10, pady=10, sticky="nw")

# Frame for buttons and search
button_frame = ttk.Frame(root, padding="10")
button_frame.grid(row=0, column=1, padx=10, pady=10, sticky="ew")

# Set up style for buttons with different colors
style = ttk.Style()

# Define styles for buttons with different colors
style.configure("Red.TButton", background="red", foreground="red", font=("Arial", 10, "bold"))
style.configure("Blue.TButton", background="blue", foreground="blue", font=("Arial", 10, "bold"))
style.configure("Green.TButton", background="green", foreground="green", font=("Arial", 10, "bold"))
style.configure("white.TButton", background="white", foreground="white", font=("Arial", 10, "bold"))




# Apply the style to the "Ajouter Client" button
add_button = ttk.Button(button_frame, text="Ajouter Client", command=lambda: open_add_client_window(root), style="Red.TButton")
add_button.grid(row=0, column=0, padx=10)

# Apply the style to other buttons
import_button = ttk.Button(button_frame, text="Importer Excel", command=import_excel, style="Blue.TButton")
import_button.grid(row=0, column=1, padx=10)

search_entry = ttk.Entry(button_frame, width=40 ,style="white.TButton", font=("Arial", 13), foreground="black")
search_entry.grid(row=0, column=2, padx=10)

search_button = ttk.Button(button_frame, text="Rechercher", command=search_client, style="Green.TButton")
search_button.grid(row=0, column=3, padx=10)

# Clear search button
clear_button = ttk.Button(button_frame, text="Effacer la recherche", command=clear_search, style="Red.TButton")
clear_button.grid(row=0, column=4, padx=10)

# Button to delete selected client
delete_button = ttk.Button(button_frame, text="Supprimer Client", command=delete_client, style="Blue.TButton")
delete_button.grid(row=0, column=5, padx=10)

# Buttom to update client
update_button = ttk.Button(button_frame, text="Modifier Client", command=update_client, style="Green.TButton")
update_button.grid(row=0, column=6, padx=10)

# Treeview for displaying client data
columns = ("ID", "N/P", "Date", "Docteur", "OD Puissance", "OG Puissance", "ADD Puissance", "Nature verre", "Société", "Prix")
tree = ttk.Treeview(root, columns=columns, show="headings", height=12)
tree.grid(row=1, column=0, columnspan=6, padx=10, pady=10)

# Configure columns 
for col in columns:
    tree.heading(col, text=col)
    tree.column(col, width=130, anchor=tk.CENTER)

# Add a tag to alternate row colors
tree.tag_configure('odd', background='white')
tree.tag_configure('even', background='#E8E8E8')

# Pagination controls
pagination_frame = ttk.Frame(root, padding="10")
pagination_frame.grid(row=2, column=0, columnspan=6, padx=10, pady=10)

prev_button = ttk.Button(pagination_frame, text="<< Précédent", command=prev_page, style="Blue.TButton")
prev_button.grid(row=0, column=0, padx=10)

pagination_label = ttk.Label(pagination_frame, text="Page 1 sur 1")
pagination_label.grid(row=0, column=1, padx=10)

next_button = ttk.Button(pagination_frame, text="Suivant >>", command=next_page, style="Blue.TButton")
next_button.grid(row=0, column=2, padx=10)

# Set the number of rows per page
rows_per_page = 10
current_page = 1
total_pages = (len(load_data()) + rows_per_page - 1) // rows_per_page

# Start with the first page of data
paginate_data()


root.mainloop()
