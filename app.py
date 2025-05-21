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

# 2. Injection CSS pour centrer titre et sous-titres
st.markdown("""
    <style>
      h1, h2, h3 { text-align: center !important; }
    </style>
    """, unsafe_allow_html=True)

# 3. Titre principal centré
st.markdown("<h1>✨Abra Cadabra✨</h1>", unsafe_allow_html=True)

# 4. Widgets d’entrée
st.header("Créer ton personnage lvl 1 !")

# Colonnes réparties également en quatre
col1, col2, col3, col4 = st.columns([2.5, 2.5, 2.5, 2.5])

with col1:
    st.markdown("**🤖 Comment t'appelles-tu ?**")
    nom = st.text_input("Nom du personnage")

with col2:
    st.markdown("**⚔️ Choisis ta posture de base**")
    posture = st.selectbox(
        "", ["──", "Posture Agressive", "Posture Defensive", "Posture Focus"], key="posture"
    )
    posture_bonuses = {
        "Posture Agressive": (
            "Tes armes infligent les dégâts max +1.\n"
            "Tes coups critiques passent à 10 %."
        ),
        "Posture Defensive": "Tu peux parer ou esquiver grâce à un jet de Physique réussi.",
        "Posture Focus": (
            "Tes sorts coûtent 1 PM en moins.\n"
            "Gagne +5 % aux caractéristiques."
        )
    }
    if posture != "──":
        st.markdown(
            f"<div style='text-align:left; white-space:pre-line; font-size:0.9rem;'>{posture_bonuses[posture]}</div>",
            unsafe_allow_html=True
        )

with col3:
    st.markdown("**🛡️ Choisis ton type de classe**")
    classe = st.selectbox(
        "", ["──", "Lourde", "Moyenne", "Légère"], key="classe"
    )
    class_info = {
        "Lourde": "+4 pv\n-2 pm\n1 sort magique",
        "Moyenne": "+1 pv\n+1 pm\n2 sorts magiques",
        "Légère": "-3 pv\n+3 pm\n3 sorts magiques"
    }
    if classe != "──":
        st.markdown(
            f"<div style='text-align:left; white-space:pre-line; font-size:0.9rem;'>{class_info[classe]}</div>",
            unsafe_allow_html=True
        )

# 5. Calcul des PV / PM selon la classe
base_pv, base_pm = 6, 4
mod_map = {"Lourde": (4, -2), "Moyenne": (1, 1), "Légère": (-2, 3)}
mod_pv, mod_pm = mod_map.get(classe, (0, 0))
pv, pm = base_pv + mod_pv, base_pm + mod_pm

with col4:
    st.markdown("**❤️ Tes PV & PM**")
    st.markdown(f"🩸 **PV → {pv}**")
    st.markdown(f"✨ **PM → {pm}**")

# 6. Quelles sont tes Statistiques ?
st.markdown("<h2>📊 Quelles sont tes Statistiques ?</h2>", unsafe_allow_html=True)
stats_col1, stats_col2, stats_col3 = st.columns(3)
with stats_col1:
    st.markdown("<h3>💪 Physique</h3>", unsafe_allow_html=True)
    physique = st.slider("", 30, 70, 30, step=5, key="physique")
with stats_col2:
    st.markdown("<h3>🧠 Mental</h3>", unsafe_allow_html=True)
    mental = st.slider("", 30, 70, 30, step=5, key="mental")
with stats_col3:
    st.markdown("<h3>🗣️ Social</h3>", unsafe_allow_html=True)
    social = st.slider("", 30, 70, 30, step=5, key="social")

# Vérification de la somme et affichage du % restant ou excédent
total_stats = physique + mental + social
if total_stats < 170:
    st.warning(f"Il reste {170 - total_stats}% à répartir.")
elif total_stats > 170:
    st.error(f"Tu as dépassé de {total_stats - 170}%. Réduis tes statistiques.")

# 7. Choisis ton alignement
st.markdown("<h2>🌗 Choisis ton Alignement</h2>", unsafe_allow_html=True)
st.markdown("**Principe et Valeurs** : Cela t'aide à incarner ton perso; pas obligé de jouer à 100 %, mais pour les actions pures conformes à tes principes, tu gagnes un bonus critique.")
alignment_options = [
    "Loyal bon — Croisé",
    "Neutre bon — Bienfaiteur",
    "Chaotique bon — Rebelle",
    "Loyal neutre — Juge",
    "Neutre strict — Réconciliateur",
    "Chaotique neutre — Esprit libre",
    "Loyal mauvais — Dominateur",
    "Neutre mauvais — Malfaisant",
    "Chaotique mauvais — Destructeur"
]
alignment = st.selectbox("", ["──"] + alignment_options, key="alignment")
if alignment != "──":
    st.markdown(f"**{alignment}**")

# 8. Choisis tes Bonus de Statistiques  
st.markdown("<h2>📝 Choisis tes Bonus de Statistiques</h2>", unsafe_allow_html=True)
skills = [
    "Discrétion +10 %", "Combats aux lames +10 %", "Artisanat +10 %", "Persuasion +10 %",
    "Tromperie +10 %", "Arcane +10 %", "Survie +10 %", "Athlétisme +10 %",
    "Perception +10 %", "Histoire +10 %", "Botanique +10 %", "Mécanisme +10 %",
    "Natation +10 %", "Pilotage +10 %", "Négociation +10 %", "Investigation +10 %",
    "Intimidation +10 %", "Danse +10 %", "Acrobatie +10 %", "Soin +10 %"
]
cols_comp = st.columns(4)
choix_competences = []
for i in range(4):
    with cols_comp[i]:
        choix = st.selectbox("", ["──"] + skills, key=f"comp{i+1}")
        if choix == "Autre":
            autres = st.text_input("Précisez autre bonus", key=f"other_bonus_{i}")
            choix_competences.append(autres)
        else:
            choix_competences.append(choix)

# 9. Choix de l'arme principale, secondaire et armure
st.markdown("<h2>🛠️  Arme & Armure</h2>", unsafe_allow_html=True)
arm_cols = st.columns(3)
with arm_cols[0]:
    st.markdown("**Arme Principale**")
    arme1 = st.selectbox("", [
        "──", "1d4 - dague/poing", "1d6 - épée/arc", "1d8 - épée longue",
        "1d10 - épée à deux mains", "1d12 - arbalète lourde", "Fusil/Pistolet (recharge mouvement)"
    ], key="arme1")
with arm_cols[1]:
    st.markdown("**Arme Secondaire**")
    arme2 = st.selectbox("", [
        "──", "1d4 - dague/poing", "1d6 - épée/arc", "1d8 - épée longue",
        "1d10 - épée à deux mains", "1d12 - arbalète lourde", "Fusil/Pistolet (recharge mouvement)"
    ], key="arme2")
with arm_cols[2]:
    st.markdown("**Type d'Armure**")
    armure = st.selectbox("", [
        "──", "Protège 3 (armure lourde)", "Protège 2 (armure moyenne)", "Protège 1 (armure légère)"
    ], key="armure")

# 10. Équipement
st.markdown("<h2>🎒 Équipement</h2>", unsafe_allow_html=True)
eq_cols = st.columns(2)
equipement_options = [
    "Corde 10m", "Torche", "Sac à dos", "Tente", "Rations (1 jour)", "Trousse de soin",
    "Bourse de pièces", "Grappin", "Plume et encre", "Livre de sorts", "Bottes de voyage",
    "Amulette de protection", "Potion de soin", "Carte de la région", "Bâton de marche",
    "Lanterne", "Tenue de camouflage", "Couteau de lancer", "Fiole d'huile", "Autre"
]
equipement = []
for col in eq_cols:
    for idx in range(4):
        key = f"equip_{eq_cols.index(col)}_{idx}"
