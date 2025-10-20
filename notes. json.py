import json

FICHIER = "notes.json"

# Charger les notes existantes
try:
    with open(FICHIER, "r") as f:
        notes = jsonn.load(f)
except FileNotFoundError:
    notes =[]

print("=== MyStudyTrack 📚 ===")

while True:
    print("\n1. Ajouter une note")
    print("2. Voir mes notes")
    print("3. Calculer la moyenne")
    print("4. Quitter")

    choix = input("Choisis une option : ")

    if choix == "1":
        matiere = input("Nom de la matière : ")
        note = float(input("Note obtenue : "))
        notes.append((matiere, note))
        with open(FICHIER, "w") as f:
            json.dump(notes, f)
        print("✅ Note enregistrée dans le fichier !")

    elif choix == "2":
        if notes:
            print("\n--- Tes notes ---")
            for m, n in notes:
                print(f"{m} : {n}/20")
        else:
            print("Aucune note enregistrée.")

    elif choix == "3":
        if notes:
            moyenne = sum(n for _, n in notes) / len(notes)
            print(f"📊 Ta moyenne est de {moyenne:.2f}/20")
            if moyenne >= 15:
                print("🎉 Excellent travail ! Continue comme ça !")
            elif moyenne >= 10:
                print("💪 Tu progresses bien, continue tes efforts !")
            else:
                print("🌱 Tu peux y arriver ! Un peu plus de révisions 💡")
        else:
            print("Ajoute d'abord des notes !")

    elif choix == "4":
                   print("👋 À bientôt dans MyStudyTrack !")
                   break
        
    else:
        print("Choix invalide. Réessaie.")
  
        print("Choix invalide. Réessaie.")
