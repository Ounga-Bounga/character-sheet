import streamlit as st

# Configuration de la page
st.set_page_config(
    page_title="Créer ton personnage niveau 1 !",
    page_icon="🎲",
    layout="wide"
)

# Titre principal
st.title("Créer ton personnage niveau 1 !")

# Mise en page en trois colonnes
col1, col2, col3 = st.columns(3)

# Colonne de gauche : saisie du nom
with col1:
    st.subheader("Comment t'appelles-tu ?")
    nom = st.text_input("Nom du personnage")

# Colonne centrale : affichage fixe du niveau
with col2:
    st.subheader("Niveau")
    st.markdown("<div style='font-size:2rem; text-align:center;'>1</div>", unsafe_allow_html=True)

# Colonne de droite : choix du type de classe
with col3:
    st.subheader("Choisis ton type de classe")
    classe = st.selectbox("", ["Lourd", "Moyen", "Léger"])
