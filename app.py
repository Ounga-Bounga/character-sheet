import streamlit as st

# 1. Configuration de la page
st.set_page_config(
    page_title="Créateur de fiche de personnage",
    page_icon="🎲",
    layout="wide",
)

# 2. CSS minimal pour centrer les titres
st.markdown("""
    <style>
      h1, h2, h3 { text-align: center !important; }
      .info-box { background: #f7f7f7; padding: 1rem; border-radius: 8px; }
    </style>
    """, unsafe_allow_html=True)

# 3. Titre principal
st.markdown("<h1>✨ Abra Cadabra ✨</h1>", unsafe_allow_html=True)

# 4. Onglets pour découper le parcours
tab_info, tab_stats, tab_skills, tab_gear = st.tabs([
    "📝 Identité & Choix",
    "📊 Statistiques",
    "⚔️ Compétences",
    "🎒 Équipement"
])

# --- Onglet 1 : Identité & Choix ---
with tab_info:
    st.header("Créer ton personnage lvl 1 !")
    col1, col2, col3, col4 = st.columns([3, 3, 3, 3])

    with col1:
        st.subheader("🤖 Nom")
        nom = st.text_input("")

    with col2:
        st.subheader("⚔️ Posture")
        posture = st.selectbox("", ["──", "Agressive", "Defensive", "Focus"])
        bonuses = {
            "Agressive": "Armes: dégâts max +1.\nCritiques: +10 %.",
            "Defensive": "Peut parer/esquiver sur jet de Physique réussi.",
            "Focus": "Sorts: -1 PM. Carac: +5 %."
        }
        if posture != "──":
            st.info(bonuses[posture])

    with col3:
        st.subheader("🛡️ Classe")
        classe = st.selectbox("", ["──", "Lourde", "Moyenne", "Légère"])
        info_classe = {
            "Lourde": "+4 PV\n-2 PM\n1 sort magique",
            "Moyenne": "+1 PV\n+1 PM\n2 sorts magiques",
            "Légère": "-3 PV\n+3 PM\n3 sorts magiques"
        }
        if classe != "──":
            st.info(info_classe[classe])

    # Calcul PV/PM immédiat
    base_pv, base_pm = 6, 4
    mods = {"Lourde": (4, -2), "Moyenne": (1, 1), "Légère": (-2, 3)}
    mod_pv, mod_pm = mods.get(classe, (0, 0))
    pv, pm = base_pv + mod_pv, base_pm + mod_pm

    with col4:
        st.subheader("❤️ PV & PM")
        st.markdown(f"🩸 **PV** → {pv}")
        st.markdown(f"✨ **PM** → {pm}")

# --- Onglet 2 : Statistiques ---
with tab_stats:
    st.header("📊 Répartition des 170 %")
    cols = st.columns(3)
    with cols[0]:
        st.subheader("💪 Physique")
        physique = st.slider(" ", 30, 70, 30, step=5, key="physique")
    with cols[1]:
        st.subheader("🧠 Mental")
        mental = st.slider(" ", 30, 70, 30, step=5, key="mental")
    with cols[2]:
        st.subheader("🗣️ Social")
        social = st.slider(" ", 30, 70, 30, step=5, key="social")

    total = physique + mental + social
    if total < 170:
        st.warning(f"Il reste {170 - total}% à répartir.")
    elif total > 170:
        st.error(f"Dépassement de {total - 170}% !")

# --- Onglet 3 : Compétences ---
with tab_skills:
    st.header("⚔️ Choisis 4 compétences (+10 %)")
    skills_list = [
        "Discrétion", "Lames", "Artisanat", "Persuasion", "Tromperie",
        "Arcane", "Survie", "Athlétisme", "Perception", "Histoire",
        "Botanique", "Mécanisme", "Natation", "Pilotage", "Négociation",
        "Investigation", "Intimidation", "Danse", "Acrobatie", "Soin"
    ]
    choix = st.multiselect(
        "", [f"{s} +10 %" for s in skills_list],
        help="Sélectionne exactement 4 compétences",
        max_selections=4
    )
    if len(choix) not in (0, 4):
        st.warning("Tu dois en choisir exactement 4.")

# --- Onglet 4 : Équipement & Armes ---
with tab_gear:
    st.header("🎒 Équipement & Armure")
    # Armes
    wa1, wa2, wa3 = st.columns(3)
    with wa1:
        st.subheader("🔹 Arme principale")
        arme1 = st.selectbox("",
            ["──","1d4 dague","1d6 épée","1d8 longue","1d10 deux mains",
             "1d12 arbalète","pistolet (recharge)"]
        )
    with wa2:
        st.subheader("🔸 Arme secondaire")
        arme2 = st.selectbox("",
            ["──","dague/poing","arc","couteau","pistolet rap."] 
        )
    with wa3:
        st.subheader("🛡️ Armure")
        armure = st.selectbox("",
            ["──","Protège 3 (lourde)","Protège 2 (moyenne)","Protège 1 (légère)"]
        )

    # Autres équipements
    st.subheader("🧰 Autres équipements")
    with st.expander("Ajouter / modifier ton équipement"):
        eq1, eq2 = st.columns(2)
        options = [
            "Corde 10m","Torche","Sac à dos","Tente","Rations",
            "Trousse de soin","Bourse de pièces","Grappin","Livre de sorts",
            "Bottes","Potion","Carte","Bâton","Lanterne","Camouflage",
            "Couteau","Fiole d'huile","Autre"
        ]
        equipment = []
        for col in (eq1, eq2):
            for _ in range(4):
                choice = col.selectbox("", ["──"] + options)
                if choice == "Autre":
                    custom = col.text_input("Précisez", "")
                    equipment.append(custom or "Autre")
                elif choice != "──":
                    equipment.append(choice)
    st.markdown(f"**Équipement choisi :** {', '.join(equipment)}")
