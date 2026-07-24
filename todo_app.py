import tkinter as tk
from tkinter import messagebox
import json
import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
FILE = os.path.join(BASE_DIR, "tasks.json")

# Fenêtre principale
root = tk.Tk()
root.title("📝 To-Do List App")
root.geometry("500x600")
root.resizable(False, False)
root.configure(bg="#f0f0f0")

# ---- Titre ----
title_label = tk.Label(
    root,
    text="📝 Ma To-Do List",
    font=("Arial", 20, "bold"),
    bg="#f0f0f0",
    fg="#333333"
)
title_label.pack(pady=20)

# ---- Champ de saisie ----
entry_frame = tk.Frame(root, bg="#f0f0f0")
entry_frame.pack(pady=10)

task_entry = tk.Entry(
    entry_frame,
    font=("Arial", 13),
    width=28,
    bd=2,
    relief="groove"
)
task_entry.pack(side="left", padx=5)

add_button = tk.Button(
    entry_frame,
    text="Ajouter",
    font=("Arial", 12, "bold"),
    bg="#4CAF50",
    fg="white",
    padx=10,
    pady=5,
    relief="flat",
    cursor="hand2"
)
add_button.pack(side="left")

# ---- Liste des tâches ----
list_frame = tk.Frame(root, bg="#f0f0f0")
list_frame.pack(pady=10)

task_listbox = tk.Listbox(
    list_frame,
    font=("Arial", 12),
    width=40,
    height=15,
    bd=2,
    relief="groove",
    selectbackground="#4CAF50",
    selectforeground="white"
)
task_listbox.pack(side="left")

scrollbar = tk.Scrollbar(list_frame)
scrollbar.pack(side="right", fill="y")

task_listbox.config(yscrollcommand=scrollbar.set)
scrollbar.config(command=task_listbox.yview)

# ---- Boutons d'action ----
btn_frame = tk.Frame(root, bg="#f0f0f0")
btn_frame.pack(pady=15)

delete_button = tk.Button(
    btn_frame,
    text="🗑️ Supprimer",
    font=("Arial", 11),
    bg="#f44336",
    fg="white",
    padx=10,
    pady=5,
    relief="flat",
    cursor="hand2"
)
delete_button.pack(side="left", padx=10)

complete_button = tk.Button(
    btn_frame,
    text="✅ Terminer",
    font=("Arial", 11),
    bg="#2196F3",
    fg="white",
    padx=10,
    pady=5,
    relief="flat",
    cursor="hand2"
)
edit_button = tk.Button(
    btn_frame,
    text="✏️ Modifier",
    font=("Arial", 11),
    bg="#FF9800",
    fg="white",
    padx=10,
    pady=5,
    relief="flat",
    cursor="hand2"
)
edit_button.pack(side="left", padx=10)
complete_button.pack(side="left", padx=10)

# ---- Fonctions ----

def load_tasks():
    if not os.path.exists(FILE):
        return []
    with open(FILE, "r") as f:
        return json.load(f)

def save_tasks(tasks):
    with open(FILE, "w") as f:
        json.dump(tasks, f, indent=4)

def refresh_listbox(tasks):
    task_listbox.delete(0, tk.END)
    for task in tasks:
        prefix = "✅ " if task["done"] else "🔲 "
        task_listbox.insert(tk.END, prefix + task["title"])

def add_task():
    title = task_entry.get().strip()
    if not title:
        messagebox.showwarning("Attention", "Écris une tâche d'abord !")
        return
    tasks = load_tasks()
    tasks.append({"title": title, "done": False})
    save_tasks(tasks)
    refresh_listbox(tasks)
    task_entry.delete(0, tk.END)

def delete_task():
    selected = task_listbox.curselection()
    if not selected:
        messagebox.showwarning("Attention", "Sélectionne une tâche d'abord !")
        return
    tasks = load_tasks()
    tasks.pop(selected[0])
    save_tasks(tasks)
    refresh_listbox(tasks)

def complete_task():
    selected = task_listbox.curselection()
    if not selected:
        messagebox.showwarning("Attention", "Sélectionne une tâche d'abord !")
        return
    tasks = load_tasks()
    tasks[selected[0]]["done"] = True
    save_tasks(tasks)
    refresh_listbox(tasks)

def edit_task():
    selected = task_listbox.curselection()
    if not selected:
        messagebox.showwarning("Attention", "Sélectionne une tâche d'abord !")
        return
    tasks = load_tasks()
    old_title = tasks[selected[0]]["title"]
    
    # Mettre l'ancien titre dans le champ de saisie
    task_entry.delete(0, tk.END)
    task_entry.insert(0, old_title)
    
    # Supprimer l'ancienne tâche
    tasks.pop(selected[0])
    save_tasks(tasks)
    refresh_listbox(tasks)

# ---- Connecter les boutons aux fonctions ----
add_button.config(command=add_task)
delete_button.config(command=delete_task)
complete_button.config(command=complete_task)
edit_button.config(command=edit_task)

# ---- Charger les tâches au démarrage ----
refresh_listbox(load_tasks())

root.mainloop()