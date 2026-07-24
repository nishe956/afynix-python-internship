import csv
import os
from datetime import datetime

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
FILE = os.path.join(BASE_DIR, "expenses.csv")

def add_expense(amount, category, description):
    file_exists = os.path.exists(FILE)
    with open(FILE, "a", newline="") as f:
        writer = csv.writer(f)
        if not file_exists:
            writer.writerow(["date", "amount", "category", "description"])
        writer.writerow([
            datetime.now().strftime("%d/%m/%Y"),
            amount,
            category,
            description
        ])
    print(f"✅ Dépense ajoutée : {amount} FCFA — {category}")

def load_expenses():
    if not os.path.exists(FILE):
        return []
    with open(FILE, "r") as f:
        reader = csv.DictReader(f)
        expenses = []
        for row in reader:
            expenses.append({
                "date": row["date"],
                "amount": float(row["amount"]),
                "category": row["category"],
                "description": row["description"]
            })
    return expenses

def show_expenses():
    expenses = load_expenses()
    if not expenses:
        print("❌ Aucune dépense enregistrée.")
        return
    print("\n📋 LISTE DES DÉPENSES :")
    print("-" * 55)
    for e in expenses:
        print(f"{e['date']} | {e['category']:15} | {e['amount']:>10.0f} FCFA | {e['description']}")
    print("-" * 55)

def category_totals():
    expenses = load_expenses()
    if not expenses:
        print("❌ Aucune dépense enregistrée.")
        return
    totals = {}
    for e in expenses:
        category = e["category"]
        if category not in totals:
            totals[category] = 0
        totals[category] += e["amount"]

    print("\n📊 TOTAUX PAR CATÉGORIE :")
    print("-" * 35)
    for category, total in totals.items():
        print(f"{category:15} : {total:>10.0f} FCFA")
    print("-" * 35)

def monthly_trends():
    expenses = load_expenses()
    if not expenses:
        print("❌ Aucune dépense enregistrée.")
        return
    months = {}
    for e in expenses:
        month = e["date"][3:]  # extrait "MM/YYYY" depuis "DD/MM/YYYY"
        if month not in months:
            months[month] = 0
        months[month] += e["amount"]

    print("\n📅 TENDANCES MENSUELLES :")
    print("-" * 35)
    for month, total in months.items():
        print(f"{month} : {total:>10.0f} FCFA")
    print("-" * 35)

def check_overspending(budget_limit):
    expenses = load_expenses()
    if not expenses:
        print("❌ Aucune dépense enregistrée.")
        return
    totals = {}
    for e in expenses:
        category = e["category"]
        if category not in totals:
            totals[category] = 0
        totals[category] += e["amount"]

    print("\n⚠️ ALERTES DE DÉPASSEMENT :")
    print("-" * 40)
    alerte_trouvee = False
    for category, total in totals.items():
        if total > budget_limit:
            print(f"🔴 {category:15} : {total:.0f} FCFA (limite : {budget_limit:.0f} FCFA)")
            alerte_trouvee = True
    if not alerte_trouvee:
        print("✅ Aucun dépassement de budget détecté.")
    print("-" * 40)


def main():
    while True:
        print("\n===== 💰 EXPENSE TRACKER =====")
        print("1. Ajouter une dépense")
        print("2. Afficher toutes les dépenses")
        print("3. Totaux par catégorie")
        print("4. Tendances mensuelles")
        print("5. Vérifier dépassement de budget")
        print("0. Quitter")
        print("==============================")

        choice = input("Votre choix : ")

        if choice == "1":
            amount = float(input("Montant (FCFA) : "))
            category = input("Catégorie (Nourriture/Transport/Loisirs...) : ")
            description = input("Description : ")
            add_expense(amount, category, description)

        elif choice == "2":
            show_expenses()

        elif choice == "3":
            category_totals()

        elif choice == "4":
            monthly_trends()

        elif choice == "5":
            limit = float(input("Budget limite par catégorie (FCFA) : "))
            check_overspending(limit)

        elif choice == "0":
            print("👋 Au revoir !")
            break

        else:
            print("❌ Choix invalide.")

main()

# TEST
add_expense(5000, "Nourriture", "Déjeuner")
add_expense(2000, "Transport", "Bus")
add_expense(15000, "Loisirs", "Cinéma")
add_expense(8000, "Nourriture", "Dîner")
check_overspending(10000)