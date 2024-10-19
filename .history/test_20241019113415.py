import tkinter as tk
from tkinter import ttk
import json

from add_client import open_add_client_window

# Chemin du fichier JSON pour sauvegarder les données
DATA_FILE = "table_data.json"

# Fonction pour charger les données à partir du fichier JSON
def load_data():
    try:
        with open(DATA_FILE, "r") as file:
            return json.load(file)
    except FileNotFoundError:
        return []  # Si le fichier n'existe pas, retourner une liste vide


# Si le fichier n'existe pas, retourner une liste vide

# Fonction pour sauvegarder les données dans un fichier JSON
def save_data():
    data = []
    for child in tree.get_children():
        data.append(tree.item(child)["values"])
    with open(DATA_FILE, "w") as file:
        json.dump(data, file)

# Fonction pour ajouter un client (ouvrir la nouvelle fenêtre)
def add_client():
    # Ouvrir la fenêtre pour ajouter un client
    def add_client_callback(new_client):
        tree.insert("", "end", values=new_client)
        save_data()
        paginate_data()

    open_add_client_window(root, add_client_callback) 

# Fonction pour rechercher un client (ici, une simple recherche par numéro de client)
def search_client():
    search_term = search_entry.get().lower()
    for child in tree.get_children():
        values = tree.item(child)["values"]
        if search_term in [str(v).lower() for v in values]:
            tree.selection_add(child)
        else:
            tree.selection_remove(child)

# Fonction pour la pagination (affichage des lignes par page)
def paginate_data():
    # Supprimer les lignes existantes dans le tableau
    for child in tree.get_children():
        tree.delete(child)
    
    # Calculer le début et la fin des données à afficher en fonction de la page actuelle
    start = (current_page - 1) * rows_per_page
    end = min(start + rows_per_page, len(all_data))
    
    # Ajouter les lignes pour la page actuelle
    for row in all_data[start:end]:
        tree.insert("", "end", values=row)
    
    # Mettre à jour les labels de pagination
    pagination_label.config(text=f"Page {current_page} sur {total_pages}")

# Charger les données et configurer la pagination
all_data = load_data()
rows_per_page = 5  # Nombre de lignes à afficher par page
current_page = 1
total_pages = (len(all_data) // rows_per_page) + 1 if len(all_data) % rows_per_page != 0 else len(all_data) // rows_per_page

# Créer la fenêtre principale
root = tk.Tk()
root.title("Tableau des informations")

# Modifier la couleur de fond de la fenêtre principale
root.configure(bg="#f0f0f0")

# Créer un cadre pour les boutons "Ajouter Client" et "Rechercher"
button_frame = ttk.Frame(root, padding="10", style="TButton")
button_frame.grid(row=0, column=0, padx=10, pady=10, sticky="ew")

# Ajouter un bouton pour "Ajouter Client"
add_button = ttk.Button(button_frame, text="Ajouter Client", command=add_client)
add_button.grid(row=0, column=0, padx=10)

# Ajouter un champ de recherche
search_entry = ttk.Entry(button_frame, width=30)
search_entry.grid(row=0, column=1, padx=10)

# Ajouter un bouton pour "Rechercher"
search_button = ttk.Button(button_frame, text="Rechercher", command=search_client)
search_button.grid(row=0, column=2, padx=10)

# Créer un cadre pour le tableau avec un padding de 10 autour
frame = ttk.Frame(root, padding="10")
frame.grid(row=1, column=0, padx=10, pady=10, sticky="nsew")

# Configurer la grille de la fenêtre principale pour qu'elle prenne tout l'espace disponible
root.grid_columnconfigure(0, weight=1)
root.grid_rowconfigure(0, weight=1)
root.grid_rowconfigure(1, weight=1)

# Créer un tableau avec les colonnes demandées
columns = ("N/P", "Date", "Docteur", "OD Puissance", "OG Puissance", "ADD Puissance", "Nature verre", "Société", "Prix")
tree = ttk.Treeview(frame, columns=columns, show="headings")

# Définir les en-têtes des colonnes
for col in columns:
    tree.heading(col, text=col)

# Définir la largeur des colonnes
tree.column("N/P", width=150)
tree.column("Date", width=150)
tree.column("Docteur", width=150)
tree.column("OD Puissance", width=100)
tree.column("OG Puissance", width=100)
tree.column("ADD Puissance", width=100)
tree.column("Nature verre", width=150)
tree.column("Société", width=150)
tree.column("Prix", width=100)

# Insertion des données dans le tableau
data = [
    ("1", "2024-10-18", "Dr. Aicha", "2.00", "1.75", "0.25", "Verre Anti-Reflet", "Société X", "150€"),
    ("1", "2024-10-18", "Dr. Aicha", "2.00", "1.75", "0.25", "Verre Anti-Reflet", "Société X", "150€"),
    ("1", "2024-10-18", "Dr. Aicha", "2.00", "1.75", "0.25", "Verre Anti-Reflet", "Société X", "150€"),
    ("1", "2024-10-18", "Dr. Aicha", "2.00", "1.75", "0.25", "Verre Anti-Reflet", "Société X", "150€"),
    ("1", "2024-10-18", "Dr. Aicha", "2.00", "1.75", "0.25", "Verre Anti-Reflet", "Société X", "150€"),
    ("1", "2024-10-18", "Dr. Aicha", "2.00", "1.75", "0.25", "Verre Anti-Reflet", "Société X", "150€"),
    ("1", "2024-10-18", "Dr. Aicha", "2.00", "1.75", "0.25", "Verre Anti-Reflet", "Société X", "150€"),
    ("1", "2024-10-18", "Dr. Aicha", "2.00", "1.75", "0.25", "Verre Anti-Reflet", "Société X", "150€"),
    ("1", "2024-10-18", "Dr. Aicha", "2.00", "1.75", "0.25", "Verre Anti-Reflet", "Société X", "150€"),
    ("1", "2024-10-18", "Dr. Aicha", "2.00", "1.75", "0.25", "Verre Anti-Reflet", "Société X", "150€"),
    ("2", "2024-10-19", "Dr. Ben", "1.50", "1.25", "0.00", "Verre Polarisé", "Société Y", "200€")
]

# Insérer les lignes dans le tableau
for row in data:
    tree.insert("", "end", values=row)

# Créer un cadre pour la pagination
pagination_frame = ttk.Frame(root, padding="10")
pagination_frame.grid(row=2, column=0, padx=10, pady=10, sticky="ew")


# Ajouter un bouton pour la page précédente
prev_button = ttk.Button(pagination_frame, text="Précédent", command=lambda: prev_page())
prev_button.grid(row=0, column=0, padx=10)

# Ajouter un label pour afficher la page actuelle
pagination_label = ttk.Label(pagination_frame, text=f"Page {current_page} sur {total_pages}")
pagination_label.grid(row=0, column=1)

# Ajouter un bouton pour la page suivante
next_button = ttk.Button(pagination_frame, text="Suivant", command=lambda: next_page())
next_button.grid(row=0, column=2, padx=10)

# Placer le tableau dans la fenêtre
tree.grid(row=0, column=0)

# Charger et afficher les données de la première page
paginate_data()

# Fonction pour la page précédente
def prev_page():
    global current_page
    if current_page > 1:
        current_page -= 1
        paginate_data()

# Fonction pour la page suivante
def next_page():
    global current_page
    if current_page < total_pages:
        current_page += 1
        paginate_data()

# Démarrer l'application
root.mainloop()
