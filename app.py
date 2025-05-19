import streamlit as st
import pandas as pd
import json

# Configuration de la page
st.set_page_config(
    page_title="Créateur de fiche de personnage",
    page_icon="🎲",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Titre et description
st.title("🎲 Créateur de fiches de personnage")
st.markdown(
    "Remplis les champs en suivant tes règles maison : répartis 170% de caractéristiques,
    choisis classe, compétences, posture, alignement, etc., puis clique sur Générer."
)

# --- Informations générales ---
st.header("Informations du personnage")
col1, col2, col3 = st.columns(3)
with col1:
    nom       = st.text_input("Nom du personnage")
    niveau    = st.number_input("Niveau", min_value=1, max_value=20, value=1, step=1)
    race      = st.selectbox("Race", ["Humain", "Elfe", "Nain", "Orc", "Autre"])
with col2:
    classe    = st.selectbox(
        "Classe (poids)",
        ["Lourd", "Moyen", "Léger"],
        help="Détermine PV/PM et armure statique"
    )
    alignement = st.selectbox(
        "Alignement",
        ["Loyal Bon", "Neutre Bon", "Chaotique Bon",
         "Loyal Neutre", "Neutre", "Chaotique Neutre",
         "Loyal Mauvais", "Neutre Mauvais", "Chaotique Mauvais"]
    )
with col3:
    st.markdown("**Principe & Alignement** donne +5% critique et +5% échec critique")

# --- Répartition des caractéristiques ---
st.header("Répartition des caractéristiques (total 170%)")
physique = st.number_input("Physique (%)", min_value=30, max_value=70, value=60, step=1)
mental   = st.number_input("Mental (%)",   min_value=30, max_value=70, value=60, step=1)
social   = st.number_input("Social (%)",   min_value=30, max_value=70, value=50, step=1)

# Vérification de la somme
total = physique + mental + social
if total != 170:
    st.error(f"La somme doit être de 170%. Actuellement : {total}%.")

# --- Sélection de compétences ---
st.header("Compétences (+10% chacune)")
skills_list = [
    "Discrétion", "Botanique", "Mécanisme", "Perception",
    "Persuasion", "Athlétisme", "Arcane", "Histoire"
]
competences = st.multiselect(
    "Choisis 4 compétences", skills_list,
    help="4 compétences maximum à +10% chacune"
)
if len(competences) != 4:
    st.error("Sélectionne exactement 4 compétences.")

# --- Choix de posture ---
st.header("Posture (état passif)")
posture = st.selectbox(
    "Posture",
    ["Aggressive ⚔️", "Défensive 🛡️", "Focus 🌀"],
    help="Chaque posture apporte un bonus spécifique"
)

# --- Calcul PV / PM et armure statique ---
base_pv, base_pm = 6, 4
mod_map = {"Lourd": (4, -2), "Moyen": (1, 1), "Léger": (-2, 3)}
armure_map = {"Lourd": 3, "Moyen": 2, "Léger": 1}
mod_pv, mod_pm = mod_map.get(classe, (0, 0))
pv = base_pv + mod_pv
pm = base_pm + mod_pm
armure = armure_map.get(classe)

# --- Nombre de dons selon la classe ---
dons_count_map = {"Lourd": 1, "Moyen": 2, "Léger": 3}
dons_count = dons_count_map.get(classe, 0)
st.header(f"Dons (tu peux en choisir {dons_count})")
don_noms = []
for i in range(dons_count):
    don = st.text_input(f"Don {i+1}")
    don_noms.append(don)

# --- Bouton Générer et affichage ---
if st.button("🖨 Générer la fiche"):
    if total != 170 or len(competences) != 4:
        st.warning("Corrige les erreurs avant de générer la fiche.")
    else:
        # Assemblage de la fiche
        fiche = {
            "Nom": nom,
            "Niveau": niveau,
            "Race": race,
            "Classe": classe,
            "Alignement": alignement,
            "Physique_%": physique,
            "Mental_%": mental,
            "Social_%": social,
            "PV": pv,
            "PM": pm,
            "Armure_Statique": armure,
            "Posture": posture,
            "Compétences": ", ".join(competences),
            "Nombre_de_dons": dons_count,
            "Dons": ", ".join([d for d in don_noms if d])
        }

        # Affichage
        st.subheader("📋 Fiche de personnage")
        df = pd.DataFrame.from_dict(fiche, orient="index", columns=["Valeur"]).reset_index()
        df.columns = ["Attribut", "Valeur"]
        st.table(df)

        # Téléchargement JSON
        st.download_button(
            label="📥 Télécharger la fiche (JSON)",
            data=json.dumps(fiche, ensure_ascii=False, indent=2),
            file_name=f"{nom or 'fiche'}_personnage.json",
            mime="application/json"
        )
