import streamlit as st

# À placer en première ligne utile du fichier
st.set_page_config(
    page_title="Mon Créateur de Fiches",
    page_icon="🎲",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Ensuite seulement : vos imports et votre code
import pandas as pd
# … le reste de votre app …

import streamlit as st
import pandas as pd
import json

# Titre de l'appli
st.title("Créateur de fiche de personnage")

st.markdown("Remplis les champs ci-dessous pour générer ta fiche.")

# ——— Champs de saisie ———
nom      = st.text_input("Nom du personnage")
race     = st.selectbox("Race", ["Humain", "Elfe", "Nain", "Orc", "Autre"])
classe   = st.selectbox("Classe", ["Guerrier", "Mage", "Voleur", "Prêtre", "Autre"])
niveau   = st.number_input("Niveau", min_value=1, max_value=20, value=1, step=1)

st.markdown("#### Caractéristiques")
force    = st.slider("Force",    1, 20, 10)
dexte    = st.slider("Dextérité",1, 20, 10)
constit  = st.slider("Constitution",1, 20, 10)
intel    = st.slider("Intelligence",1, 20, 10)
sagesse  = st.slider("Sagesse",   1, 20, 10)
charis   = st.slider("Charisme",  1, 20, 10)

# Bouton pour générer la fiche
if st.button("🖨 Générer la fiche"):
    # On assemble les données dans un dict
    fiche = {
        "Nom"         : nom,
        "Race"        : race,
        "Classe"      : classe,
        "Niveau"      : niveau,
        "Force"       : force,
        "Dextérité"   : dexte,
        "Constitution": constit,
        "Intelligence": intel,
        "Sagesse"     : sagesse,
        "Charisme"    : charis
    }

    # Affichage de la fiche
    st.subheader("🎲 Fiche de personnage")
    df = pd.DataFrame.from_dict(fiche, orient="index", columns=["Valeur"])
    st.table(df)

    # Option : proposer le téléchargement en JSON
    st.download_button(
        label="📥 Télécharger la fiche (JSON)",
        data=json.dumps(fiche, ensure_ascii=False, indent=2),
        file_name=f"{nom or 'fiche'}_personnage.json",
        mime="application/json"
    )
