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
    mental   = st.slider("",   30, 70, 30, step=5, key="mental")
with stats_col3:
    st.markdown("<h3>🗣️ Social</h3>", unsafe_allow_html=True)
    social   = st.slider("",   30, 70, 30, step=5, key="social")

# Vérification de la somme et affichage du % restant ou excédent
total_stats = physique + mental + social
if total_stats < 170:
    st.warning(f"Il reste {170 - total_stats}% à répartir.")
elif total_stats > 170:
    st.error(f"Tu as dépassé de {total_stats - 170}%. Réduis tes statistiques.")

# 7. Choisis tes compétences
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
        choix = st.selectbox(f"Compétence {i+1}", ["──"] + skills, key=f"comp{i+1}")
        choix_competences.append(choix)

# 8. Choix de l'arme principale, arme secondaire et équipement
st.markdown("<h2>🛠️ Armes & Équipement</h2>", unsafe_allow_html=True)
wa_col1, wa_col2 = st.columns(2)
with wa_col1:
    st.markdown("**Choisis ton arme principale**")
    weapon_opts = [
        "──", "1d4 - dague/poing", "1d6 - épée/arc", "1d8 - épée longue",
        "1d10 - épée à deux mains", "1d12 - arbalète lourde", "fusil/pistolet (recharge mouvement)"
    ]
    arme_principale = st.selectbox("", weapon_opts, key="arme_principale")
    st.markdown("**Choisis ton arme secondaire**")
    arme_secondaire = st.selectbox("", weapon_opts, key="arme_secondaire")

with wa_col2:
    st.markdown("**Choisis ton équipement**")
    equip_opts = [
        "──", "Torche", "Corde (10m)", "Sac à dos", "Trousse de soins",
        "Potion de soin", "Parchemin magique", "Crochet", "Bourse d'or",
        "Sac de couchage", "Couteau de chasse", "Rations (1 jour)", "Jumelles",
        "Carte de la région", "Bétail de poche", "Hachette", "Flèches (20)",
        "Étui à sorts", "Lettre scellée", "Autre"
    ]
    eq_1 = st.selectbox("Slot 1", equip_opts, key="eq1")
    eq_2 = st.selectbox("Slot 2", equip_opts, key="eq2")
    eq_3 = st.selectbox("Slot 3", equip_opts, key="eq3")
    eq_4 = st.selectbox("Slot 4", equip_opts, key="eq4")
    st.markdown("---")
    # Deuxième colonne d'équipement
    eq_5 = st.selectbox("Slot 5", equip_opts, key="eq5")
    eq_6 = st.selectbox("Slot 6", equip_opts, key="eq6")
    eq_7 = st.selectbox("Slot 7", equip_opts, key="eq7")
    eq_8 = st.selectbox("Slot 8", equip_opts, key="eq8")

# (le reste de ton code suit ici...)
