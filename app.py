import streamlit as st

st.set_page_config(
    page_title="Créer ton personnage niveau 1 !",
    page_icon="🎲",
    layout="wide"
)

# Injection CSS pour centrer automatiquement tous les <h3>
st.markdown(
    """
    <style>
      h3 { text-align: center; }
    </style>
    """,
    unsafe_allow_html=True
)

st.title("Créer ton personnage niveau 1 !")

# Trois colonnes côte à côte
col1, col2, col3 = st.columns(3)

with col1:
    st.markdown("<h3>🤖 Comment t'appelles-tu ?</h3>", unsafe_allow_html=True)
    nom = st.text_input("Nom du personnage")

with col2:
    st.markdown("<h3>🎚️ Niveau</h3>", unsafe_allow_html=True)
    # Centré inline pour plus de contrôle
    st.markdown("<div style='font-size:2rem; text-align:center;'>1</div>", unsafe_allow_html=True)

with col3:
    st.markdown("<h3>🛡️ Choisis ton type de classe</h3>", unsafe_allow_html=True)
    classe = st.selectbox("", ["Lourd", "Moyen", "Léger"])
