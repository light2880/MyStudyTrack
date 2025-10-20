import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import json
import os

st.set_page_config(page_title="MyStudyTrack", layout="wide")
st.title("📚 MyStudyTrack - Suivi intelligent des notes")

# ---------------------------
# 🔹 Chargement / sauvegarde des données
# ---------------------------
FICHIER = "notes.json"

if os.path.exists(FICHIER):
    with open(FICHIER, "r") as f:
        notes_data = json.load(f)
else:
    notes_data = []

# Stockage dans session_state pour garder les données pendant la session
if 'notes' not in st.session_state:
    st.session_state.notes = notes_data

# ---------------------------
# 1️⃣ Ajouter une note
# ---------------------------
st.header("✏️ Ajouter une note")

with st.form("ajout_note_unique"):
    matiere = st.text_input("Matière")
    note = st.number_input("Note obtenue", 0.0, 20.0)
    coef = st.number_input("Coefficient", 1, 10)
    submitted = st.form_submit_button("Ajouter la note")

    if submitted:
        if matiere:
            st.session_state.notes.append({"matiere": matiere, "note": note, "coef": coef})
            with open(FICHIER, "w") as f:
                json.dump(st.session_state.notes, f, indent=4)
            st.success(f"✅ Note ajoutée : {note}/20 en {matiere} (coef {coef})")
        else:
            st.error("⚠️ Merci d’indiquer une matière avant d’ajouter la note.")

# ---------------------------
# 2️⃣ Afficher les notes et moyennes
# ---------------------------
st.header("📖 Mes notes et moyennes")

if st.session_state.notes:
    df_notes = pd.DataFrame(st.session_state.notes)
    st.dataframe(df_notes, use_container_width=True)

    # Moyenne générale pondérée
    moyenne_generale = (df_notes["note"] * df_notes["coef"]).sum() / df_notes["coef"].sum()
    st.subheader(f"📊 Moyenne générale : {moyenne_generale:.2f}/20")

    # Moyenne par matière
    moyennes_matieres = df_notes.groupby("matiere").apply(
        lambda x: (x["note"] * x["coef"]).sum() / x["coef"].sum()
    )
    st.write("### Moyenne par matière :")
    for matiere, moyenne in moyennes_matieres.items():
        emoji = "🟢" if moyenne >= 10 else "🔴"
        st.write(f"{emoji} **{matiere}** → {moyenne:.2f}/20")

else:
    st.info("Aucune note enregistrée pour l’instant.")

# ---------------------------
# 3️⃣ Graphiques d’évolution
# ---------------------------
st.header("📈 Graphiques de progression")

if st.session_state.notes:
    fig, ax = plt.subplots()
    moyennes_matieres.plot(kind="bar", ax=ax, color="#4e79a7", edgecolor="black")
    ax.set_ylim(0, 20)
    ax.set_ylabel("Note moyenne")
    ax.set_title("Moyenne par matière")
    st.pyplot(fig)
else:
    st.warning("Ajoute d’abord des notes pour voir un graphique.")

# ---------------------------
# 4️⃣ Calculateur de rattrapage
# ---------------------------
st.header("🎯 Calculateur de note pour atteindre la moyenne")

moyenne_actuelle = st.number_input("Ta moyenne actuelle dans la matière", min_value=0.0, max_value=20.0, key="moy_act")
coeff_actuelle = st.number_input("Somme des coefficients déjà notés", min_value=1, key="coef_act")
coeff_restante = st.number_input("Coefficient de la prochaine note", min_value=1, key="coef_rest")
moyenne_cible = st.number_input("Moyenne que tu veux atteindre", min_value=0.0, max_value=20.0, key="moy_cible")

if st.button("Calculer la note à obtenir"):
    note_requise = (moyenne_cible * (coeff_actuelle + coeff_restante) - moyenne_actuelle * coeff_actuelle) / coeff_restante
    note_requise = max(0, min(note_requise, 20))
    st.success(f"🎯 Pour atteindre {moyenne_cible}/20, tu dois obtenir : **{note_requise:.2f}/20** à la prochaine évaluation.")


