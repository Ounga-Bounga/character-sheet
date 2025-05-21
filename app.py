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
# Swap : colonne 1 = Nom, colonne 2 = Classe, colonne 3 = Niveau
col1, col2, col3 = st.columns([4, 4, 2])  # 40% / 40% / 20%

with col1:
    st.markdown("<h3>🤖 Comment t'appelles-tu ?</h3>", unsafe_allow_html=True)
    nom = st.text_input("Nom du personnage")

with col2:
    st.markdown("<h3>🛡️ Choisis ton type de classe</h3>", unsafe_allow_html=True)
    classe = st.selectbox("", ["Lourd", "Moyen", "Léger"])

with col3:
    st.markdown("<h3>Niveau</h3>", unsafe_allow_html=True)
    # Affichage du niveau dans un petit bloc
    st.markdown(
        "<div style='border:1px solid #ddd; "
        "padding:0.5rem; border-radius:4px; "
        "text-align:center; font-size:1.5rem; "
        "font-weight:bold;'>1</div>",
        unsafe_allow_html=True
    )

# (le reste du code suit...)
