import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

st.set_page_config(page_title="MyStudyTrack", layout="wide")
st.title("📚 MyStudyTrack - Suivi de mes notes")

# ---------------------------
# 1️⃣ Gestion des notes
# ---------------------------
st.header("Mes notes")

if 'notes' not in st.session_state:
    st.session_state.notes = []

with st.form("ajout_note_unique"):
    matiere = st.text_input("Matière")
    note = st.number_input("Note obtenue", 0.0, 20.0)
    coef = st.number_input("Coefficient", 1, 10)
    submitted = st.form_submit_button("Ajouter la note")
    if submitted:
        if matiere:
            st.session_state.notes.append((matiere, note, coef))
            st.success(f"✅ Note ajoutée : {note}/20 en {matiere} (coef {coef})")
        else:
            st.error("⚠️ Merci d’indiquer une matière avant d’ajouter la note.")

# --- Affichage des notes ---
if st.session_state.notes:
    df_notes = pd.DataFrame(st.session_state.notes, columns=["Matière", "Note", "Coefficient"])
    st.dataframe(df_notes, use_container_width=True)

    # Moyenne pondérée
    moyenne = (df_notes["Note"] * df_notes["Coefficient"]).sum() / df_notes["Coefficient"].sum()
    st.subheader(f"📊 Moyenne générale : {moyenne:.2f}/20")
else:
    st.info("Aucune note enregistrée pour l’instant.")

# ---------------------------
# 2️⃣ Graphiques d’évolution
# ---------------------------
st.header("📈 Graphiques d’évolution")
if st.session_state.notes:
    fig, ax = plt.subplots()
    df_notes.groupby("Matière")["Note"].mean().plot(kind="bar", ax=ax, color="#4e79a7", edgecolor="black")
    ax.set_ylim(0, 20)
    ax.set_ylabel("Note moyenne")
    ax.set_title("Notes par matière")
    st.pyplot(fig)
else:
    st.warning("Ajoute d’abord des notes pour voir un graphique.")

# ---------------------------
# 3️⃣ Calculateur de rattrapage
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
