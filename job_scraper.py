import requests
import json
import csv
import os
import pandas as pd

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

def fetch_jobs(keyword="python"):
    print(f"\n🔍 Recherche des offres pour : {keyword}...")
    url = f"https://remotive.com/api/remote-jobs?search={keyword}&limit=10"
    
    response = requests.get(url)
    
    if response.status_code == 200:
        data = response.json()
        jobs = data["jobs"]
        print(f"✅ {len(jobs)} offres trouvées !")
        return jobs
    else:
        print(f"❌ Erreur : {response.status_code}")
        return []

def save_to_csv(jobs, filename="jobs.csv"):
    path = os.path.join(BASE_DIR, filename)
    with open(path, "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(["title", "company", "location", "url", "date"])
        for job in jobs:
            writer.writerow([
                job["title"],
                job["company_name"],
                job["candidate_required_location"],
                job["url"],
                job["publication_date"][:10]  # garde seulement la date sans l'heure
            ])
    print(f"💾 {len(jobs)} offres sauvegardées dans jobs.csv")

def save_to_json(jobs, filename="jobs.json"):
    path = os.path.join(BASE_DIR, filename)
    data = []
    for job in jobs:
        data.append({
            "title": job["title"],
            "company": job["company_name"],
            "location": job["candidate_required_location"],
            "url": job["url"],
            "date": job["publication_date"][:10]
        })
    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=4, ensure_ascii=False)
    print(f"💾 {len(jobs)} offres sauvegardées dans jobs.json")

def display_jobs(filename="jobs.csv"):
    path = os.path.join(BASE_DIR, filename)
    df = pd.read_csv(path)
    print(f"\n📋 LISTE DES OFFRES ({len(df)} résultats) :")
    print("-" * 80)
    for _, row in df.iterrows():
        print(f"💼 {row['title']}")
        print(f"   🏢 {row['company']} | 📍 {row['location']} | 📅 {row['date']}")
        print(f"   🔗 {row['url']}")
        print()

def filter_jobs(keyword, filename="jobs.csv"):
    path = os.path.join(BASE_DIR, filename)
    df = pd.read_csv(path)
    
    # cherche le mot clé dans le titre ou la localisation
    filtered = df[
        df["title"].str.contains(keyword, case=False, na=False) |
        df["location"].str.contains(keyword, case=False, na=False)
    ]
    
    if filtered.empty:
        print(f"❌ Aucune offre trouvée pour '{keyword}'")
        return
    
    print(f"\n🔎 {len(filtered)} offre(s) trouvée(s) pour '{keyword}' :")
    print("-" * 80)
    for _, row in filtered.iterrows():
        print(f"💼 {row['title']}")
        print(f"   🏢 {row['company']} | 📍 {row['location']} | 📅 {row['date']}")
        print(f"   🔗 {row['url']}")
        print()

def main():
    while True:
        print("\n===== 💼 JOB LISTING AGGREGATOR =====")
        print("1. Rechercher des offres d'emploi")
        print("2. Afficher toutes les offres sauvegardées")
        print("3. Filtrer les offres par mot-clé")
        print("0. Quitter")
        print("=====================================")

        choice = input("Votre choix : ")

        if choice == "1":
            keyword = input("Mot-clé de recherche (ex: python, data, developer) : ")
            jobs = fetch_jobs(keyword)
            if jobs:
                save_to_csv(jobs)
                save_to_json(jobs)
                display_jobs()

        elif choice == "2":
            display_jobs()

        elif choice == "3":
            keyword = input("Filtrer par mot-clé (ex: Worldwide, USA, Senior) : ")
            filter_jobs(keyword)

        elif choice == "0":
            print("👋 Au revoir !")
            break

        else:
            print("❌ Choix invalide.")

main()



