import streamlit as st
import pandas as pd
import json

# 1. Configuration de la page
st.set_page_config(
    page_title="Créer ton personnage niveau 1 !",
    page_icon="🎲",
    layout="wide",
    initial_sidebar_state="expanded"
)

# 2. Injection CSS globale (centres h1/h3 + styles de la fiche)
st.markdown("""
<style>
/* Centrage des titres */
h1, h3 { text-align: center !important; }

/* RAZ marges listes */
ul, li {
  margin: 0;
  padding: 0;
  list-style: none;
}

/* Header flex */
.header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  margin-bottom: 1rem;
}
.header h2 {
  margin: 0;
  font-size: 2rem;
  font-weight: 600;
}
.header img {
  border-radius: 8px;
  object-fit: cover;
}

/* Liste PV/PM */
.header ul {
  margin-left: 1rem;
}
.header ul li {
  display: list-item;
  list-style-type: disc;
  margin-left: 1rem;
  font-size: 1rem;
}

/* Blocs caractéristiques */
.section-box {
  display: inline-block;
  width: 32%;
  padding: 0.75rem 0;
  border-radius: 8px;
  text-align: center;
  font-weight: 500;
  margin-right: 1%;
  margin-bottom: 1rem;
}
.section-box:last-child { margin-right: 0; }
.physique { background-color: #f8d0d0; }
.mental   { background-color: #d0e0f8; }
.social   { background-color: #f8f0d0; }
.section-box h3 { margin: 0; font-size: 1.25rem; }
.section-box p { margin: 0.25rem 0 0; font-size: 1.5rem; font-weight: 600; }

/* Alignement */
.alignement {
  text-align: center;
  font-style: italic;
  margin: 0.5rem 0 1.5rem;
  font-size: 0.9rem;
  color: #555;
}

/* Séparateur */
.separator {
  border-top: 1px solid #ddd;
  margin: 1rem 0;
}

/* Compétences */
.skills {
  display: flex;
  justify-content: space-between;
  gap: 1rem;
  margin-bottom: 2rem;
}
.skills > div { flex: 1; }

/* Dons & Équipement */
.dons-equip {
  display: flex;
  gap: 2rem;
  margin-top: 2rem;
}
.dons-equip .block {
  flex: 1;
}
.dons-equip .block h4 {
  margin-bottom: 0.5rem;
  font-size: 1.25rem;
  font-weight: 500;
}
.dons-equip .block ul {
  list-style-type: disc;
  margin-left: 1rem;
}
</style>
""", unsafe_allow_html=True)

# 3. Titre principal centré
st.markdown("<h1>Créer ton personnage niveau 1 !</h1>", unsafe_allow_html=True)

# 4. Section de création (trois colonnes 40%/40%/20%)
st.header("Création du personnage")
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
        "<div style='border:1px solid #ddd; padding:0.5rem; "
        "border-radius:4px; text-align:center; "
        "font-size:1.5rem; font-weight:bold;'>1</div>",
        unsafe_allow_html=True
    )

# 5. Répartition des caractéristiques
physique = st.slider("Physique (%)", 30, 70, 60)
mental   = st.slider("Mental (%)",   30, 70, 60)
social   = st.slider("Social (%)",   30, 70, 50)
total    = physique + mental + social
if total != 170:
    st.error(f"Somme = {total} %, doit faire 170 %")

# 6. Compétences (+10 % chacune)
skills_list  = ["Discrétion", "Botanique", "Mécanisme", "Perception",
                "Persuasion", "Athlétisme", "Arcane", "Histoire"]
competences  = st.multiselect("Choisis 4 compétences (+10 %)", skills_list)
if len(competences) not in (0, 4):
    st.warning("Sélectionne exactement 4 compétences")

# 7. Dons selon la classe
dons_count_map = {"Lourd":1, "Moyen":2, "Léger":3}
don_noms      = [st.text_input(f"Don {i+1}") for i in range(dons_count_map[classe])]

# 8. Équipement (une ligne par item)
equipement_list = st.text_area(
    "Équipement (une ligne par item)",
    "1d6 - bâton\n1d12 - pistolet\nhabits, kit, tente"
).splitlines()

# 9. Calcul PV / PM / Armure
base_pv, base_pm = 6, 4
mod_pv, mod_pm   = {"Lourd":(4,-2), "Moyen":(1,1), "Léger":(-2,3)}[classe]
pv, pm           = base_pv + mod_pv, base_pm + mod_pm
armure           = {"Lourd":3, "Moyen":2, "Léger":1}[classe]

# 10. Affichage de l’en-tête détaillé de la fiche
image_url = "https://...ton-image.png"
st.markdown(f"""
<div class="header">
  <h2>{nom or '–'} lvl 1</h2>
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
  {alignement} — esprit libre +5 % coup / échec critique
</div>
<div class="separator"></div>
""", unsafe_allow_html=True)

# 11. Compétences en dropdowns horizontaux
st.markdown("#### Compétences (+10 %)")
st.markdown('<div class="skills">', unsafe_allow_html=True)
for i, skill in enumerate(competences):
    st.selectbox("", [f"{skill} 10 %"], key=f"skill_{i}")
st.markdown('</div>', unsafe_allow_html=True)

# 12. Séparateur avant Dons/Équipement
st.markdown('<div class="separator"></div>', unsafe_allow_html=True)

# 13. Dons & Équipement en deux colonnes
st.markdown('<div class="dons-equip">', unsafe_allow_html=True)

# Dons
st.markdown('<div class="block">', unsafe_allow_html=True)
st.subheader("Dons")
for don in don_noms:
    if don:
        st.write(f"- {don}")
st.markdown('</div>', unsafe_allow_html=True)

# Équipement
st.markdown('<div class="block">', unsafe_allow_html=True)
st.subheader("Équipement")
for item in equipement_list:
    st.write(f"- {item}")
st.markdown('</div>', unsafe_allow_html=True)

# Fin container Dons/Équipement
st.markdown('</div>', unsafe_allow_html=True)
