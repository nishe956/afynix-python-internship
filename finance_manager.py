import tkinter as tk
from tkinter import messagebox, ttk
import csv
import os
from datetime import datetime

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
FILE = os.path.join(BASE_DIR, "transactions.csv")

# Fenêtre principale
root = tk.Tk()
root.title("💰 Personal Finance Manager")
root.geometry("700x600")
root.resizable(False, False)
root.configure(bg="#f5f5f5")

# ---- Titre ----
title_label = tk.Label(
    root,
    text="💰 Personal Finance Manager",
    font=("Arial", 18, "bold"),
    bg="#f5f5f5",
    fg="#333333"
)
title_label.pack(pady=15)
# ---- Formulaire ----
form_frame = tk.Frame(root, bg="#ffffff", bd=2, relief="groove")
form_frame.pack(pady=10, padx=20, fill="x")

tk.Label(form_frame, text="Type :", font=("Arial", 11), bg="#ffffff").grid(row=0, column=0, padx=10, pady=8)
type_var = tk.StringVar(value="Revenu")
type_menu = ttk.Combobox(form_frame, textvariable=type_var, values=["Revenu", "Dépense"], width=15, state="readonly")
type_menu.grid(row=0, column=1, padx=10, pady=8)

tk.Label(form_frame, text="Montant (FCFA) :", font=("Arial", 11), bg="#ffffff").grid(row=0, column=2, padx=10)
amount_entry = tk.Entry(form_frame, font=("Arial", 11), width=15, bd=2, relief="groove")
amount_entry.grid(row=0, column=3, padx=10)

tk.Label(form_frame, text="Catégorie :", font=("Arial", 11), bg="#ffffff").grid(row=1, column=0, padx=10, pady=8)
category_entry = tk.Entry(form_frame, font=("Arial", 11), width=15, bd=2, relief="groove")
category_entry.grid(row=1, column=1, padx=10)

tk.Label(form_frame, text="Description :", font=("Arial", 11), bg="#ffffff").grid(row=1, column=2, padx=10)
desc_entry = tk.Entry(form_frame, font=("Arial", 11), width=15, bd=2, relief="groove")
desc_entry.grid(row=1, column=3, padx=10)

add_button = tk.Button(
    form_frame,
    text="➕ Ajouter",
    font=("Arial", 11, "bold"),
    bg="#4CAF50",
    fg="white",
    padx=15,
    pady=5,
    relief="flat",
    cursor="hand2"
)
add_button.grid(row=2, column=0, columnspan=4, pady=10)
# ---- Tableau des transactions ----
table_frame = tk.Frame(root, bg="#f5f5f5")
table_frame.pack(pady=10, padx=20, fill="both")

columns = ("date", "type", "montant", "categorie", "description")
tree = ttk.Treeview(table_frame, columns=columns, show="headings", height=10)

tree.heading("date", text="📅 Date")
tree.heading("type", text="📌 Type")
tree.heading("montant", text="💵 Montant")
tree.heading("categorie", text="🏷️ Catégorie")
tree.heading("description", text="📝 Description")

tree.column("date", width=100, anchor="center")
tree.column("type", width=80, anchor="center")
tree.column("montant", width=120, anchor="center")
tree.column("categorie", width=120, anchor="center")
tree.column("description", width=180, anchor="center")

tree_scroll = ttk.Scrollbar(table_frame, orient="vertical", command=tree.yview)
tree.configure(yscrollcommand=tree_scroll.set)

tree.pack(side="left", fill="both")
tree_scroll.pack(side="right", fill="y")

# ---- Résumé ----
summary_frame = tk.Frame(root, bg="#f5f5f5")
summary_frame.pack(pady=5, padx=20, fill="x")

income_label = tk.Label(summary_frame, text="💚 Revenus : 0 FCFA", font=("Arial", 11, "bold"), bg="#f5f5f5", fg="#4CAF50")
income_label.pack(side="left", padx=20)

expense_label = tk.Label(summary_frame, text="🔴 Dépenses : 0 FCFA", font=("Arial", 11, "bold"), bg="#f5f5f5", fg="#f44336")
expense_label.pack(side="left", padx=20)

balance_label = tk.Label(summary_frame, text="💰 Solde : 0 FCFA", font=("Arial", 11, "bold"), bg="#f5f5f5", fg="#2196F3")
balance_label.pack(side="left", padx=20)

# ---- Fonctions ----

def load_transactions():
    if not os.path.exists(FILE):
        return []
    with open(FILE, "r", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        return list(reader)

def save_transaction(transaction):
    file_exists = os.path.exists(FILE)
    with open(FILE, "a", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=["date", "type", "montant", "categorie", "description"])
        if not file_exists:
            writer.writeheader()
        writer.writerow(transaction)

def refresh_table():
    for row in tree.get_children():
        tree.delete(row)
    transactions = load_transactions()
    total_income = 0
    total_expense = 0
    for t in transactions:
        montant = float(t["montant"])
        if t["type"] == "Revenu":
            total_income += montant
            tree.insert("", "end", values=(t["date"], t["type"], f"{montant:.0f} FCFA", t["categorie"], t["description"]), tags=("income",))
        else:
            total_expense += montant
            tree.insert("", "end", values=(t["date"], t["type"], f"{montant:.0f} FCFA", t["categorie"], t["description"]), tags=("expense",))
    tree.tag_configure("income", foreground="#4CAF50")
    tree.tag_configure("expense", foreground="#f44336")
    balance = total_income - total_expense
    income_label.config(text=f"💚 Revenus : {total_income:.0f} FCFA")
    expense_label.config(text=f"🔴 Dépenses : {total_expense:.0f} FCFA")
    balance_label.config(text=f"💰 Solde : {balance:.0f} FCFA")

def add_transaction():
    t_type = type_var.get()
    montant = amount_entry.get().strip()
    categorie = category_entry.get().strip()
    description = desc_entry.get().strip()

    if not montant or not categorie or not description:
        messagebox.showwarning("Attention", "Remplis tous les champs !")
        return
    try:
        montant = float(montant)
    except ValueError:
        messagebox.showerror("Erreur", "Le montant doit être un nombre !")
        return

    transaction = {
        "date": datetime.now().strftime("%d/%m/%Y"),
        "type": t_type,
        "montant": montant,
        "categorie": categorie,
        "description": description
    }
    save_transaction(transaction)
    refresh_table()
    amount_entry.delete(0, tk.END)
    category_entry.delete(0, tk.END)
    desc_entry.delete(0, tk.END)
    messagebox.showinfo("Succès", "Transaction ajoutée !")

# ---- Connecter le bouton ----
add_button.config(command=add_transaction)

# ---- Charger les transactions au démarrage ----
refresh_table()

# ---- Fonctions ----

def load_transactions():
    if not os.path.exists(FILE):
        return []
    with open(FILE, "r", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        return list(reader)

def save_transaction(transaction):
    file_exists = os.path.exists(FILE)
    with open(FILE, "a", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=["date", "type", "montant", "categorie", "description"])
        if not file_exists:
            writer.writeheader()
        writer.writerow(transaction)


def add_transaction():
    t_type = type_var.get()
    montant = amount_entry.get().strip()
    categorie = category_entry.get().strip()
    description = desc_entry.get().strip()

    if not montant or not categorie or not description:
        messagebox.showwarning("Attention", "Remplis tous les champs !")
        return
    try:
        montant = float(montant)
    except ValueError:
        messagebox.showerror("Erreur", "Le montant doit être un nombre !")
        return

    transaction = {
        "date": datetime.now().strftime("%d/%m/%Y"),
        "type": t_type,
        "montant": montant,
        "categorie": categorie,
        "description": description
    }
    save_transaction(transaction)
    refresh_table()
    amount_entry.delete(0, tk.END)
    category_entry.delete(0, tk.END)
    desc_entry.delete(0, tk.END)
    messagebox.showinfo("Succès", "Transaction ajoutée !")

# ---- Connecter le bouton ----
add_button.config(command=add_transaction)

# ---- Charger les transactions au démarrage ----
refresh_table()

# ---- Boutons d'action ----
action_frame = tk.Frame(root, bg="#f5f5f5")
action_frame.pack(pady=10)

delete_button = tk.Button(
    action_frame,
    text="🗑️ Supprimer",
    font=("Arial", 11, "bold"),
    bg="#f44336",
    fg="white",
    padx=15,
    pady=5,
    relief="flat",
    cursor="hand2"
)
delete_button.pack(side="left", padx=10)

report_button = tk.Button(
    action_frame,
    text="📊 Rapport mensuel",
    font=("Arial", 11, "bold"),
    bg="#2196F3",
    fg="white",
    padx=15,
    pady=5,
    relief="flat",
    cursor="hand2"
)
report_button.pack(side="left", padx=10)
yearly_button = tk.Button(
    action_frame,
    text="📅 Rapport annuel",
    font=("Arial", 11, "bold"),
    bg="#9C27B0",
    fg="white",
    padx=15,
    pady=5,
    relief="flat",
    cursor="hand2"
)
yearly_button.pack(side="left", padx=10)


# ---- Fonctions des boutons ----
def delete_transaction():
    selected = tree.selection()
    if not selected:
        messagebox.showwarning("Attention", "Sélectionne une transaction d'abord !")
        return
    item = tree.item(selected[0])
    values = item["values"]
    transactions = load_transactions()
    transactions = [t for t in transactions if not (
        t["date"] == values[0] and
        t["type"] == values[1] and
        t["description"] == values[4]
    )]
    with open(FILE, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=["date", "type", "montant", "categorie", "description"])
        writer.writeheader()
        writer.writerows(transactions)
    refresh_table()
    messagebox.showinfo("Succès", "Transaction supprimée !")

def monthly_report():
    transactions = load_transactions()
    if not transactions:
        messagebox.showinfo("Rapport", "Aucune transaction enregistrée.")
        return
    months = {}
    for t in transactions:
        month = t["date"][3:]  # extrait MM/YYYY
        if month not in months:
            months[month] = {"revenus": 0, "depenses": 0}
        if t["type"] == "Revenu":
            months[month]["revenus"] += float(t["montant"])
        else:
            months[month]["depenses"] += float(t["montant"])

    report = "📊 RAPPORT MENSUEL\n"
    report += "=" * 35 + "\n"
    for month, data in months.items():
        balance = data["revenus"] - data["depenses"]
        report += f"\n📅 {month}\n"
        report += f"  💚 Revenus  : {data['revenus']:.0f} FCFA\n"
        report += f"  🔴 Dépenses : {data['depenses']:.0f} FCFA\n"
        report += f"  💰 Solde    : {balance:.0f} FCFA\n"

    messagebox.showinfo("Rapport Mensuel", report)

delete_button.config(command=delete_transaction)
report_button.config(command=monthly_report)

def yearly_report():
    transactions = load_transactions()
    if not transactions:
        messagebox.showinfo("Rapport", "Aucune transaction enregistrée.")
        return
    years = {}
    for t in transactions:
        year = t["date"][6:]  # extrait YYYY
        if year not in years:
            years[year] = {"revenus": 0, "depenses": 0}
        if t["type"] == "Revenu":
            years[year]["revenus"] += float(t["montant"])
        else:
            years[year]["depenses"] += float(t["montant"])

    report = "📊 RAPPORT ANNUEL\n"
    report += "=" * 35 + "\n"
    for year, data in years.items():
        balance = data["revenus"] - data["depenses"]
        report += f"\n📅 {year}\n"
        report += f"  💚 Revenus  : {data['revenus']:.0f} FCFA\n"
        report += f"  🔴 Dépenses : {data['depenses']:.0f} FCFA\n"
        report += f"  💰 Solde    : {balance:.0f} FCFA\n"

    messagebox.showinfo("Rapport Annuel", report)
yearly_button.config(command=yearly_report)  # ← ajoute cette ligne
# ---- Search & Filter ----
search_frame = tk.Frame(root, bg="#f5f5f5")
search_frame.pack(pady=5, padx=20, fill="x")

tk.Label(search_frame, text="🔍 Rechercher :", font=("Arial", 11), bg="#f5f5f5").pack(side="left")
search_entry = tk.Entry(search_frame, font=("Arial", 11), width=20, bd=2, relief="groove")
search_entry.pack(side="left", padx=10)

def search_transactions():
    keyword = search_entry.get().strip().lower()
    for row in tree.get_children():
        tree.delete(row)
    transactions = load_transactions()
    for t in transactions:
        if (keyword in t["categorie"].lower() or
            keyword in t["description"].lower() or
            keyword in t["type"].lower()):
            montant = float(t["montant"])
            tag = "income" if t["type"] == "Revenu" else "expense"
            tree.insert("", "end", values=(
                t["date"], t["type"],
                f"{montant:.0f} FCFA",
                t["categorie"],
                t["description"]
            ), tags=(tag,))

search_button = tk.Button(
    search_frame,
    text="🔍 Chercher",
    font=("Arial", 11, "bold"),
    bg="#FF9800",
    fg="white",
    padx=10,
    pady=3,
    relief="flat",
    cursor="hand2",
    command=search_transactions
)
search_button.pack(side="left")

reset_button = tk.Button(
    search_frame,
    text="🔄 Reset",
    font=("Arial", 11, "bold"),
    bg="#607D8B",
    fg="white",
    padx=10,
    pady=3,
    relief="flat",
    cursor="hand2",
    command=refresh_table
)
reset_button.pack(side="left", padx=5)
root.mainloop()