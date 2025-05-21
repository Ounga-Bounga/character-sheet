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

# 2. Injection CSS pour centrer le titre principal
st.markdown(
    """
    <style>
      h1 { text-align: center !important; }
    </style>
    """,
    unsafe_allow_html=True
)

# 3. Titre principal centré
st.markdown("<h1>Créer ton personnage niveau 1 !</h1>", unsafe_allow_html=True)

# 4. Widgets d’entrée
st.header("Création du personnage")
# Colonnes 40% / 40% / 20%
col1, col2, col3 = st.columns([4, 4, 2])

with col1:
    st.markdown("<h3>🤖 Comment t'appelles-tu ?</h3>", unsafe_allow_html=True)
    nom = st.text_input("Nom du personnage")

with col2:
    st.markdown("<h3>🛡️ Choisis ton type de classe</h3>", unsafe_allow_html=True)
    classe = st.selectbox("", ["Lourd", "Moyen", "Léger"])

with col3:
    st.markdown("<h3>Niveau</h3>", unsafe_allow_html=True)
    st.markdown(
        "<div style='"
        "border:1px solid #ddd; padding:0.5rem; border-radius:4px; "
        "text-align:center; font-size:1.5rem; font-weight:bold;"
        "'>1</div>",
        unsafe_allow_html=True
    )

# 5. Calcul des PV / PM selon la classe
base_pv, base_pm = 6, 4
mod_map = {
    "Lourd": (4, -2),
    "Moyen": (1,  1),
    "Léger": (-2, 3)
}
mod_pv, mod_pm = mod_map[classe]
pv = base_pv + mod_pv
pm = base_pm + mod_pm

# 6. Affichage des points de vie et de magie sous le nom
with col1:
    st.markdown(f"🩸 **Tes points de vie → {pv}**")
    st.markdown(f"✨ **Tes points de magie → {pm}**")

# (le reste de ton code suit ici...)
