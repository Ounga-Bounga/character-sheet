import streamlit as st
import pandas as pd
import json

# 1. Configuration de la page
st.set_page_config(
    page_title="Créateur de fiche de personnage",
    page_icon="🎲",
    layout="wide",
    initial_sidebar_state="expanded"
)

# 2. Injection CSS pour centrer le titre principal et les sous-titres
st.markdown(
    """
    <style>
      h1, h2, h3 { text-align: center !important; }
    </style>
    """,
    unsafe_allow_html=True
)

# 3. Titre principal centré
st.markdown("<h1>Créer ton personnage niveau 1 !</h1>", unsafe_allow_html=True)

# 4. Widgets d’entrée
st.header("Création du personnage")
# Colonnes réparties 30% / 30% / 30% / 10%
col1, col2, col3, col4 = st.columns([3, 3, 3, 1])

with col1:
    st.markdown("<h3>🤖 Comment t'appelles-tu ?</h3>", unsafe_allow_html=True)
    nom = st.text_input("Nom du personnage")

with col2:
    st.markdown("<h3>🛡️ Choisis ton type de classe</h3>", unsafe_allow_html=True)
    classe = st.selectbox("", ["Lourde", "Moyenne", "Légère"])

with col3:
    st.markdown("<h3>⚔️ Choisis ta posture de base</h3>", unsafe_allow_html=True)
    posture = st.selectbox(
        "",
        ["Posture Agressive", "Posture Defensive", "Posture Focus"]
    )
    posture_bonuses = {
        "Posture Agressive": "Tes armes infligent les dégâts max +1. Tes chances de coups critiques passent à 10%.",
        "Posture Defensive": "Tu peux parer/esquiver une attaque en réussissant un jet de Physique.",
        "Posture Focus": "Tes sorts coûtent 1 point de magie en moins. Gagne +5% à tes caractéristiques."
    }
    st.markdown(
        f"<p style='text-align:left; font-size:0.9rem;'>{posture_bonuses[posture]}</p>",
        unsafe_allow_html=True
    )

with col4:
    st.markdown("<h3>Niveau</h3>", unsafe_allow_html=True)
    st.markdown(
        "<div style='border:1px solid #ddd; padding:0.5rem; border-radius:4px;"
        " text-align:center; font-size:1.5rem; font-weight:bold;'>1</div>",
        unsafe_allow_html=True
    )

# 5. Calcul des PV / PM selon la classe
base_pv, base_pm = 6, 4
mod_map = {
    "Lourde": (4, -2),
    "Moyenne": (1,  1),
    "Légère": (-2, 3)
}
mod_pv, mod_pm = mod_map[classe]
pv = base_pv + mod_pv
pm = base_pm + mod_pm

# 6. Affichage des points de vie et de magie sous le nom
with col1:
    st.markdown(f"🩸 **Tes points de vie → {pv}**")
    st.markdown(f"✨ **Tes points de magie → {pm}**")

# 7. Quelles sont tes Statistiques ?
st.markdown("<h2>📊 Quelles sont tes Statistiques ?</h2>", unsafe_allow_html=True)
stats_col1, stats_col2, stats_col3 = st.columns(3)
# Jauges sliders pour répartir 170%, max 70%
with stats_col1:
    physique = st.slider("Physique (%)", 30, 70, 30, step=1)
with stats_col2:
    mental   = st.slider("Mental (%)",   30, 70, 30, step=1)
with stats_col3:
    social   = st.slider("Social (%)",   30, 70, 30, step=1)
# Vérification de la somme des stats
total_stats = physique + mental + social
if total_stats != 170:
    st.error(f"La somme des statistiques doit être de 170%, actuellement {total_stats}%.")

# 8. Choisis tes compétences
st.markdown("<h2>📝 Choisis tes compétences (+10%)</h2>", unsafe_allow_html=True)
skills = [
    "Discrétion +10%", "Combats aux lames +10%", "Artisanat +10%", "Persuasion +10%",
    "Tromperie +10%", "Arcane +10%", "Survie +10%", "Athlétisme +10%",
    "Perception +10%", "Histoire +10%", "Botanique +10%", "Mécanisme +10%",
    "Natation +10%", "Pilotage +10%", "Négociation +10%", "Investigation +10%",
    "Intimidation +10%", "Danse +10%", "Acrobatie +10%", "Soin +10%"
]
cols_comp = st.columns(4)
choix_competences = []
for i in range(4):
    with cols_comp[i]:
        choix = st.selectbox(f"Compétence {i+1}", ["──"] + skills, key=f"comp{i+1}")
        choix_competences.append(choix)

# (le reste de ton code suit ici...)
