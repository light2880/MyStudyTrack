import streamlit as st
import json
import os
import matplotlib.pyplot as plt

FICHIER = "notes.json"

# --- Charger les données ---
if os.path.exists(FICHIER):
    with open(FICHIER, "r") as f:
        notes = json.load(f)
else:
    notes = []

st.title("🎓 MyStudyTrack Web")

# --- Ajouter une note ---
st.subheader("Ajouter une note")
with st.form("form_ajouter"):
    matiere = st.text_input("Matière")
    note = st.number_input("Note /20", min_value=0.0, max_value=20.0, step=0.5)
    coef = st.number_input("Coefficient", min_value=1, step=1)
    submit = st.form_submit_button("➕ Ajouter la note")
    if submit:
        if matiere:
            notes.append((matiere, note, coef))
            with open(FICHIER, "w") as f:
                json.dump(notes, f, indent=4)
            st.success(f"Note ajoutée : {matiere} → {note}/20 (coef {coef})")
        else:
            st.error("Entre un nom de matière.")

# --- Supprimer une note ---
st.subheader("Supprimer une note")
if notes:
    matieres_notes = [f"{m} : {n}/20 (coef {c})" for m, n, c in notes]
    selection = st.selectbox("Sélectionne une note à supprimer", matieres_notes)
    if st.button("🗑️ Supprimer la note"):
        index = matieres_notes.index(selection)
        notes.pop(index)
        with open(FICHIER, "w") as f:
            json.dump(notes, f, indent=4)
        st.success("Note supprimée avec succès !")
else:
    st.write("Aucune note enregistrée.")

# --- Afficher les notes ---
st.subheader("Mes notes")
if notes:
    for m, n, c in notes:
        st.write(f"📌 {m} : {n}/20 (coef {c})")
else:
    st.write("Aucune note enregistrée.")

# --- Calculer la moyenne pondérée ---
if st.button("📊 Calculer la moyenne"):
    if notes:
        somme_notes = sum(n*c for _, n, c in notes)
        somme_coefs = sum(c for _, _, c in notes)
        moyenne = somme_notes / somme_coefs
        st.success(f"📈 Moyenne pondérée : {moyenne:.2f}/20")
    else:
        st.warning("Aucune note pour calculer la moyenne.")

# --- Afficher graphique ---
if st.button("📈 Afficher graphique"):
    if notes:
        matieres = [m for m, _, _ in notes]
        valeurs = [n for _, n, _ in notes]
        plt.figure(figsize=(8,4))
        plt.bar(matieres, valeurs, color="#007acc", edgecolor="black")
        plt.title("Mes notes par matière", fontsize=14)
        plt.xlabel("Matières")
        plt.ylabel("Notes /20")
        plt.ylim(0, 20)
        plt.grid(axis='y', linestyle="--", alpha=0.6)
        st.pyplot(plt)
    else:
        st.warning("Aucune note à afficher.")

import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

st.set_page_config(page_title="MyStudyTrack", layout="wide")
st.title("📚 MyStudyTrack - Suivi de mes notes")

# ---------------------------
# 1️⃣ Gestion des notes
# ---------------------------
st.header("Mes notes")

# Exemple : dictionnaire pour stocker les notes
if 'notes' not in st.session_state:
    st.session_state.notes = []

with st.form("ajout_note"):
    matiere = st.text_input("Matière")
    note = st.number_input("Note obtenue", 0.0, 20.0)
    coef = st.number_input("Coefficient", 1, 10)
    submitted = st.form_submit_button("Ajouter la note")
    if submitted:
        st.session_state.notes.append((matiere, note, coef))
        st.success(f"Note ajoutée : {note}/20 en {matiere} (coef {coef})")

# Affichage des notes
if st.session_state.notes:
    df_notes = pd.DataFrame(st.session_state.notes, columns=["Matière", "Note", "Coefficient"])
    st.dataframe(df_notes)

    # Moyenne pondérée
    moyenne = (df_notes["Note"] * df_notes["Coefficient"]).sum() / df_notes["Coefficient"].sum()
    st.subheader(f"Moyenne générale : {moyenne:.2f}/20")

# ---------------------------
# 2️⃣ Graphiques
# ---------------------------
st.header("Graphiques d’évolution")
if st.session_state.notes:
    fig, ax = plt.subplots()
    df_notes.groupby("Matière")["Note"].mean().plot(kind="bar", ax=ax)
    ax.set_ylim(0, 20)
    ax.set_ylabel("Note moyenne")
    ax.set_title("Notes par matière")
    st.pyplot(fig)

# ---------------------------
# 3️⃣ Calculateur de rattrapage
# ---------------------------
st.header("Calculateur de note pour atteindre la moyenne")

moyenne_actuelle = st.number_input("Moyenne actuelle de la matière", min_value=0.0, max_value=20.0, key="moy_act")
coeff_actuelle = st.number_input("Somme des coefficients déjà notés", min_value=1, key="coef_act")
coeff_restante = st.number_input("Coefficient de la prochaine note", min_value=1, key="coef_rest")
moyenne_cible = st.number_input("Moyenne souhaitée", min_value=0.0, max_value=20.0, key="moy_cible")

if st.button("Calculer la note à obtenir"):
    note_requise = (moyenne_cible * (coeff_actuelle + coeff_restante) - moyenne_actuelle * coeff_actuelle) / coeff_restante
    note_requise = max(0, min(note_requise, 20))
    st.success(f"Pour atteindre {moyenne_cible}/20, tu dois obtenir : {note_requise:.2f}/20")
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

st.set_page_config(page_title="MyStudyTrack", layout="wide")
st.title("📚 MyStudyTrack - Suivi de mes notes")

# ---------------------------
# 1️⃣ Gestion des notes
# ---------------------------
st.header("Mes notes")

# Exemple : dictionnaire pour stocker les notes
if 'notes' not in st.session_state:
    st.session_state.notes = []

with st.form("ajout_note"):
    matiere = st.text_input("Matière")
    note = st.number_input("Note obtenue", 0.0, 20.0)
    coef = st.number_input("Coefficient", 1, 10)
    submitted = st.form_submit_button("Ajouter la note")
    if submitted:
        st.session_state.notes.append((matiere, note, coef))
        st.success(f"Note ajoutée : {note}/20 en {matiere} (coef {coef})")

# Affichage des notes
if st.session_state.notes:
    df_notes = pd.DataFrame(st.session_state.notes, columns=["Matière", "Note", "Coefficient"])
    st.dataframe(df_notes)

    # Moyenne pondérée
    moyenne = (df_notes["Note"] * df_notes["Coefficient"]).sum() / df_notes["Coefficient"].sum()
    st.subheader(f"Moyenne générale : {moyenne:.2f}/20")

# ---------------------------
# 2️⃣ Graphiques
# ---------------------------
st.header("Graphiques d’évolution")
if st.session_state.notes:
    fig, ax = plt.subplots()
    df_notes.groupby("Matière")["Note"].mean().plot(kind="bar", ax=ax)
    ax.set_ylim(0, 20)
    ax.set_ylabel("Note moyenne")
    ax.set_title("Notes par matière")
    st.pyplot(fig)

# ---------------------------
# 3️⃣ Calculateur de rattrapage
# ---------------------------
st.header("Calculateur de note pour atteindre la moyenne")

moyenne_actuelle = st.number_input("Moyenne actuelle de la matière", min_value=0.0, max_value=20.0, key="moy_act")
coeff_actuelle = st.number_input("Somme des coefficients déjà notés", min_value=1, key="coef_act")
coeff_restante = st.number_input("Coefficient de la prochaine note", min_value=1, key="coef_rest")
moyenne_cible = st.number_input("Moyenne souhaitée", min_value=0.0, max_value=20.0, key="moy_cible")

if st.button("Calculer la note à obtenir"):
    note_requise = (moyenne_cible * (coeff_actuelle + coeff_restante) - moyenne_actuelle * coeff_actuelle) / coeff_restante
    note_requise = max(0, min(note_requise, 20))
    st.success(f"Pour atteindre {moyenne_cible}/20, tu dois obtenir : {note_requise:.2f}/20")
