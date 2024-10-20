import tkinter as tk
from tkinter import ttk

def open_add_client_window(parent, add_client_callback):
    add_window = tk.Toplevel(parent)
    add_window.title("Ajouter un nouveau client")

    # Création des champs du formulaire
    /
    labels = ["N/P", "Date", "Docteur", "OD Puissance", "OG Puissance", "ADD Puissance", "Nature verre", "Société", "Prix"]
    entries = {}

    for i, label in enumerate(labels):
        tk.Label(add_window, text=label).grid(row=i, column=0, padx=10, pady=5)
        entry = ttk.Entry(add_window)
        entry.grid(row=i, column=1, padx=10, pady=5)
        entries[label] = entry

    # Fonction appelée lors de l'ajout du client
    def submit_client():
        client_data = [entries[label].get() for label in labels]
        add_client_callback(client_data)  # Appelle la fonction de callback pour ajouter les données au tableau
        add_window.destroy()  # Ferme la fenêtre après l'ajout

    # Bouton de soumission
    submit_button = ttk.Button(add_window, text="Ajouter", command=submit_client)
    submit_button.grid(row=len(labels), column=0, columnspan=2, pady=10)

    add_window.transient(parent)  # Associe cette fenêtre à la fenêtre principale
    add_window.grab_set()  # Empêche d'interagir avec la fenêtre principale tant que celle-ci n'est pas fermée
    parent.wait_window(add_window)  # Attendre la fermeture de cette fenêtre avant de continuer

