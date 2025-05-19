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

# 2. Widgets d’entrée
st.header("Création du personnage")
nom        = st.text_input("Nom du personnage")
niveau     = st.number_input("Niveau", 1, 20, 1)
race       = st.selectbox("Race", ["Humain","Elfe","Nain","Orc","Autre"])
classe     = st.selectbox("Classe (poids)", ["Lourd","Moyen","Léger"])
posture    = st.selectbox("Posture de base", ["Aggressive ⚔️","Défensive 🛡️","Focus 🌀"])
alignement = st.selectbox("Alignement", [
    "Loyal Bon","Neutre Bon","Chaotique Bon",
    "Loyal Neutre","Neutre","Chaotique Neutre",
    "Loyal Mauvais","Neutre Mauvais","Chaotique Mauvais"
])

# Répartition des caractéristiques
physique = st.slider("Physique (%)", 30, 70, 60)
mental   = st.slider("Mental (%)",   30, 70, 60)
social   = st.slider("Social (%)",   30, 70, 50)
total    = physique + mental + social
if total != 170:
    st.error(f"Somme = {total}%, doit faire 170%")

# Compétences (4 max)
skills_list  = ["Discrétion","Botanique","Mécanisme","Perception",
                "Persuasion","Athlétisme","Arcane","Histoire"]
competences  = st.multiselect("Choisis 4 compétences (+10%)", skills_list)
if len(competences) not in (0, 4):
    st.warning("Sélectionne exactement 4 compétences")

# Dons selon la classe
dons_count_map = {"Lourd":1,"Moyen":2,"Léger":3}
don_noms = [st.text_input(f"Don {i+1}") for i in range(dons_count_map[classe])]

# Équipement (une ligne par item)
equipement_list = st.text_area(
    "Équipement (une ligne par item)",
    "1d6 - bâton\n1d12 - pistolet\nhabits, kit, tente"
).splitlines()

# Calcul PV / PM / Armure
base_pv, base_pm = 6, 4
mod_pv, mod_pm   = {"Lourd":(4,-2),"Moyen":(1,1),"Léger":(-2,3)}[classe]
pv, pm           = base_pv + mod_pv, base_pm + mod_pm
armure           = {"Lourd":3,"Moyen":2,"Léger":1}[classe]

# 3. Injection CSS
st.markdown("""
<style>
/* ... ton CSS comme précédemment ... */
</style>
""", unsafe_allow_html=True)

# 4. Affichage de l’en-tête et des blocs colorés
image_url = "https://...ton-image.png"
st.markdown(f"""
<div class="header">
  <h2>{nom or '–'} lvl {niveau}</h2>
  <img src="{image_url}" width="150"/>
</div>
<ul>
  <li>{pv} PV</li>
  <li>{pm} PM</li>
  <li>Classe : {classe}</li>
  <li>Posture de base : {posture}</li>
</ul>
<div class="section-box physique">
  <h3>Physique</h3><p>{physique} %</p>
</div>
<div class="section-box mental">
  <h3>Mental</h3><p>{mental} %</p>
</div>
<div class="section-box social">
  <h3>Social</h3><p>{social} %</p>
</div>
<div class="alignement">
  {alignement} — esprit libre +5% critique/échec
</div>
""", unsafe_allow_html=True)

# 5. Compétences en dropdown horizontal
st.markdown("#### Compétences (+10%)")
cols = st.columns(4)
for i, skill in enumerate(competences):
    cols[i].selectbox("", [f"{skill} 10%"], key=f"skill_{i}")

# 6. Dons & Équipement en deux colonnes
col1, col2 = st.columns(2, gap="large")
with col1:
    st.subheader("Dons")
    for don in don_noms:
        if don:
            st.write(f"- {don}")
with col2:
    st.subheader("Équipement")
    for item in equipement_list:
        st.write(f"- {item}")
