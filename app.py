import streamlit as st
import pandas as pd
import json

# 1. Config de la page
st.set_page_config(
    page_title="Créateur de fiche de personnage",
    page_icon="🎲",
    layout="wide",
    initial_sidebar_state="expanded"
)

# 2. Widgets d’entrée
st.header("Création du personnage")
nom       = st.text_input("Nom du personnage")
niveau    = st.number_input("Niveau", 1, 20, 1)
race      = st.selectbox("Race", ["Humain","Elfe","Nain","Orc","Autre"])
classe    = st.selectbox("Classe (poids)", ["Lourd","Moyen","Léger"])
alignement= st.selectbox("Alignement", [
    "Loyal Bon","Neutre Bon","Chaotique Bon",
    "Loyal Neutre","Neutre","Chaotique Neutre",
    "Loyal Mauvais","Neutre Mauvais","Chaotique Mauvais"
])
# Caractéristiques
physique  = st.slider("Physique (%)",   30,70,60)
mental    = st.slider("Mental (%)",     30,70,60)
social    = st.slider("Social (%)",     30,70,50)
# Validation somme
total = physique+mental+social
if total != 170:
    st.error(f"Somme = {total}%, doit faire 170%")

# Compétences et dons
skills_list = ["Discrétion","Botanique","Mécanisme","Perception",
               "Persuasion","Athlétisme","Arcane","Histoire"]
competences = st.multiselect("Choisis 4 compétences (+10%)", skills_list)
dons_count  = {"Lourd":1,"Moyen":2,"Léger":3}[classe]
don_noms    = [st.text_input(f"Don {i+1}") for i in range(dons_count)]

# Équipement
equipement_list = st.text_area(
    "Équipement (une ligne par item)",
    value="1d6 - bâton\n1d12 - pistolet\nhabits, kit, tente"
).splitlines()

# Calcul PV/PM/armure
base_pv,base_pm = 6,4
mod_pv,mod_pm   = {"Lourd":(4,-2),"Moyen":(1,1),"Léger":(-2,3)}[classe]
pv, pm          = base_pv+mod_pv, base_pm+mod_pm
armure          = {"Lourd":3,"Moyen":2,"Léger":1}[classe]

# 3. Injection CSS
st.markdown("""
<style> 
  /* ton CSS ici… */ 
</style>
""", unsafe_allow_html=True)

# 4. Affichage HTML/CSS
image_url = "https://…ton-image.png"
st.markdown(f"""
<div class="header">
  <h2>{nom or '–'} lvl {niveau}</h2>
  <img src="{image_url}" width="150"/>
</div>
<ul>
  <li>{pv} PV</li>
  <li>{pm} PM</li>
  <li>Classe : {classe}</li>
  <li>Posture : {posture}</li>
</ul>
<div class="section-box physique"><h3>Physique</h3><p>{physique}%</p></div>
<div class="section-box mental">  <h3>Mental</h3>  <p>{mental}%</p></div>
<div class="section-box social">  <h3>Social</h3>  <p>{social}%</p></div>
<div class="alignement">{alignement} — esprit libre +5% critique/échec</div>
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
        st.write(f"- {don}")
with col2:
    st.subheader("Équipement")
    for item in equipement_list:
        st.write(f"- {item}")
