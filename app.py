import streamlit as st
import json
from typing import List, Dict, Tuple

# =========================
# Config
# =========================
st.set_page_config(
    page_title="Créateur de fiche de personnage",
    page_icon="🎲",
    layout="wide",
    initial_sidebar_state="expanded",
)

# =========================
# Styles
# =========================
st.markdown(
    """
    <style>
      h1, h2, h3 { text-align: center !important; }
      .muted { opacity: 0.8; font-size: 0.9rem; }
      .card {
        border-radius: 16px; padding: 1rem 1.2rem; border: 1px solid #e7e7e9;
        box-shadow: 0 1px 8px rgba(0,0,0,0.04); background: white; margin-bottom: .75rem;
      }
      .mono { font-family: ui-monospace, SFMono-Regular, Menlo, Monaco, Consolas, "Liberation Mono", "Courier New", monospace;}
      .grid { display: grid; grid-template-columns: repeat(auto-fit, minmax(220px,1fr)); gap: .75rem; }
    </style>
    """,
    unsafe_allow_html=True,
)

# =========================
# Constants
# =========================
POSTURES: Dict[str, str] = {
    "Posture Agressive": "• Armes: dégâts max +1\n• Critiques: passe à 10 %",
    "Posture Defensive": "• Peut parer/esquiver sur jet de Physique réussi",
    "Posture Focus": "• Sorts coûtent 1 PM en moins\n• +5 % à toutes les caractéristiques",
}

CLASSES = {
    "Lourde": {"pv_mod": +4, "pm_mod": -2, "sorts": 1, "desc": "+4 PV | -2 PM | 1 sort"},
    "Moyenne": {"pv_mod": +1, "pm_mod": +1, "sorts": 2, "desc": "+1 PV | +1 PM | 2 sorts"},
    "Légère": {"pv_mod": -3, "pm_mod": +3, "sorts": 3, "desc": "-3 PV | +3 PM | 3 sorts"},
}

BASE_PV, BASE_PM = 6, 4
STATS_MIN, STATS_MAX, STATS_STEP, STATS_TOTAL = 30, 70, 5, 170

ALIGNMENTS = [
    "Loyal bon — Croisé",
    "Neutre bon — Bienfaiteur",
    "Chaotique bon — Rebelle",
    "Loyal neutre — Juge",
    "Neutre strict — Réconciliateur",
    "Chaotique neutre — Esprit libre",
    "Loyal mauvais — Dominateur",
    "Neutre mauvais — Malfaisant",
    "Chaotique mauvais — Destructeur",
]

SKILLS = [
    "Discrétion +10 %", "Combats aux lames +10 %", "Artisanat +10 %", "Persuasion +10 %",
    "Tromperie +10 %", "Arcane +10 %", "Survie +10 %", "Athlétisme +10 %",
    "Perception +10 %", "Histoire +10 %", "Botanique +10 %", "Mécanisme +10 %",
    "Natation +10 %", "Pilotage +10 %", "Négociation +10 %", "Investigation +10 %",
    "Intimidation +10 %", "Danse +10 %", "Acrobatie +10 %", "Soin +10 %", "Autre"
]

WEAPONS = [
    "1d4 - dague/poing", "1d6 - épée/arc", "1d8 - épée longue",
    "1d10 - épée à deux mains", "1d12 - arbalète lourde", "Fusil/Pistolet (recharge mouvement)"
]

ARMORS = ["Protège 3 (armure lourde)", "Protège 2 (armure moyenne)", "Protège 1 (armure légère)"]

EQUIPMENT = [
    "Corde 10m", "Torche", "Sac à dos", "Tente", "Rations (1 jour)", "Trousse de soin",
    "Bourse de pièces", "Grappin", "Plume et encre", "Livre de sorts", "Bottes de voyage",
    "Amulette de protection", "Potion de soin", "Carte de la région", "Bâton de marche",
    "Lanterne", "Tenue de camouflage", "Couteau de lancer", "Fiole d'huile", "Autre"
]

# =========================
# Title
# =========================
st.markdown("<h1>✨ Abra Cadabra ✨</h1>", unsafe_allow_html=True)
st.header("Créer ton personnage lvl 1 !")

# =========================
# Helpers
# =========================
def compute_hp_mp(class_key: str) -> Tuple[int, int]:
    mods = CLASSES.get(class_key, {"pv_mod": 0, "pm_mod": 0})
    return BASE_PV + mods["pv_mod"], BASE_PM + mods["pm_mod"]

def clean_choices(choices: List[str]) -> List[str]:
    """Removes placeholders and empties, keeps unique order."""
    out, seen = [], set()
    for c in choices:
        c = (c or "").strip()
        if not c or c == "──":
            continue
        if c not in seen:
            seen.add(c)
            out.append(c)
    return out

# =========================
# PREVIEW SECTIONS (infos AVANT choix)
# =========================
st.markdown("### 📘 Comprendre vos choix (avant de sélectionner)")
# Postures preview
with st.expander("⚔️ Postures — effets détaillés", expanded=True):
    st.markdown("<div class='grid'>", unsafe_allow_html=True)
    for name, desc in POSTURES.items():
        st.markdown(f"<div class='card'><b>{name}</b><br><span class='muted'>{desc.replace(chr(10), '<br>')}</span></div>", unsafe_allow_html=True)
    st.markdown("</div>", unsafe_allow_html=True)

# Classes preview with computed totals
with st.expander("🛡️ Classes — PV/PM & sorts", expanded=True):
    st.markdown(
        f"<div class='muted'>Base: <span class='mono'>PV {BASE_PV} / PM {BASE_PM}</span>. "
        f"Les valeurs ci-dessous montrent le total <i>après</i> modificateurs de classe.</div>",
        unsafe_allow_html=True,
    )
    st.markdown("<div class='grid'>", unsafe_allow_html=True)
    for name, meta in CLASSES.items():
        pv, pm = compute_hp_mp(name)
        st.markdown(
            f"<div class='card'><b>{name}</b><br>"
            f"<div>PV totaux: <span class='mono'>{pv}</span> &nbsp;|&nbsp; PM totaux: <span class='mono'>{pm}</span></div>"
            f"<div class='muted'>{meta['desc']} • Sorts à choisir: {meta['sorts']}</div></div>",
            unsafe_allow_html=True,
        )
    st.markdown("</div>", unsafe_allow_html=True)

# Stats rules preview
with st.expander("📊 Règles des caractéristiques (Physique / Mental / Social)", expanded=True):
    st.markdown(
        f"""
        <div class='card'>
          <ul>
            <li>Chaque caractéristique varie de <b>{STATS_MIN}%</b> à <b>{STATS_MAX}%</b> (pas de {STATS_STEP}%).</li>
            <li>La somme <b>doit</b> faire exactement <b>{STATS_TOTAL}%</b>.</li>
            <li>Certains choix (ex: <i>Posture Focus</i>) peuvent donner <b>+5%</b> aux caractéristiques.</li>
          </ul>
          <div class='muted'>Astuce: commence à 30/30/30 puis répartis le reste vers ton style de jeu.</div>
        </div>
        """,
        unsafe_allow_html=True,
    )

# =========================
# Form
# =========================
with st.form("builder", clear_on_submit=False):
    col1, col2, col3, col4 = st.columns(4)

    with col1:
        st.markdown("**🤖 Comment t'appelles-tu ?**")
        nom = st.text_input("Nom du personnage", key="nom")

    with col2:
        st.markdown("**⚔️ Choisis ta posture de base**")
        posture = st.selectbox("Posture", ["──"] + list(POSTURES.keys()), key="posture")

        # Indication visible AVANT/pendant le choix (persistante)
        if posture == "──":
            st.info("Sélectionne une posture. Voir le détail dans « Postures — effets détaillés » ci-dessus.")
        else:
            st.markdown(
                f"<div class='card'><div style='white-space:pre-line;'>{POSTURES[posture]}</div></div>",
                unsafe_allow_html=True
            )

    with col3:
        st.markdown("**🛡️ Choisis ton type de classe**")
        classe = st.selectbox("Classe", ["──"] + list(CLASSES.keys()), key="classe")

        # Indication visible AVANT/pendant le choix (persistante)
        if classe == "──":
            st.info("Sélectionne une classe. Les PV/PM totaux et le nombre de sorts sont indiqués au-dessus.")
        else:
            pv_preview, pm_preview = compute_hp_mp(classe)
            st.markdown(
                f"<div class='card'>PV totaux: <span class='mono'>{pv_preview}</span> • "
                f"PM totaux: <span class='mono'>{pm_preview}</span><br>"
                f"<span class='muted'>{CLASSES[classe]['desc']} • Sorts: {CLASSES[classe]['sorts']}</span></div>",
                unsafe_allow_html=True,
            )

    with col4:
        # Affiche PV/PM en temps réel selon la classe
        pv, pm = compute_hp_mp(classe) if classe != "──" else (BASE_PV, BASE_PM)
        st.markdown("**❤️ Tes PV & PM (aperçu)**")
        st.metric("🩸 PV", pv)
        st.metric("✨ PM", pm)

    # ====== Stats
    st.markdown("<h2>📊 Choisis tes Caractéristiques</h2>", unsafe_allow_html=True)
    st.caption("Lis d'abord les règles ci-dessus — la somme doit être exactement 170 %.")

    stats_col1, stats_col2, stats_col3 = st.columns(3)
    with stats_col1:
        physique = st.slider("💪 Physique", STATS_MIN, STATS_MAX, 30, step=STATS_STEP, key="physique")
    with stats_col2:
        mental = st.slider("🧠 Mental", STATS_MIN, STATS_MAX, 30, step=STATS_STEP, key="mental")
    with stats_col3:
        social = st.slider("🗣️ Social", STATS_MIN, STATS_MAX, 30, step=STATS_STEP, key="social")

    total_stats = physique + mental + social
    remaining = STATS_TOTAL - total_stats
    if remaining > 0:
        st.info(f"Il reste {remaining}% à répartir.")
    elif remaining < 0:
        st.error(f"Tu as dépassé de {-remaining}%. Réduis tes statistiques.")
    else:
        st.success("Parfait, tu es à 170 %.")

    # ====== Alignement
    st.markdown("<h2>🌗 Choisis ton Alignement</h2>", unsafe_allow_html=True)
    st.markdown(
        "<div class='muted'>Pour des actions conformes à tes principes, tu peux obtenir un bonus critique.</div>",
        unsafe_allow_html=True,
    )
    alignment = st.selectbox("Alignement", ["──"] + ALIGNMENTS, key="alignment")

    # ====== Compétences
    st.markdown("<h2>📝 Choisis tes Bonus de Compétences</h2>", unsafe_allow_html=True)
    comp_cols = st.columns(4)
    selected_skills: List[str] = []
    for i in range(4):
        with comp_cols[i]:
            choix = st.selectbox(f"Compétence {i+1}", ["──"] + SKILLS, key=f"comp{i+1}")
            if choix == "Autre":
                autre = st.text_input("Précisez", key=f"comp_autre_{i}")
                if autre:
                    selected_skills.append(autre.strip())
            else:
                selected_skills.append(choix)
    selected_skills = clean_choices(selected_skills)
    if len(selected_skills) < 4:
        st.warning("Sélectionne 4 compétences uniques (ou précise tes 'Autre').")

    # ====== Sorts
    sorts = []
    num_sorts = CLASSES.get(classe, {"sorts": 0}).get("sorts", 0) if classe != "──" else 0
    if num_sorts > 0:
        st.markdown("<h2>🪄 Choisis tes Sorts</h2>", unsafe_allow_html=True)
        sort_cols = st.columns(num_sorts)
        for idx, col in enumerate(sort_cols):
            with col:
                st.markdown(f"**Sort {idx+1}**")
                nom_sort = st.text_input(f"Nom du sort {idx+1}", key=f"nom_sort_{idx}")
                cout_pm = st.number_input(f"Coût en PM (sort {idx+1})", min_value=0, step=1, key=f"cout_sort_{idx}")
                desc_sort = st.text_area(f"Description du sort {idx+1}", key=f"desc_sort_{idx}")
                if nom_sort:
                    sorts.append({"nom": nom_sort.strip(), "cout_pm": int(cout_pm), "description": desc_sort.strip()})
        if len(sorts) < num_sorts:
            st.info(f"Renseigne {num_sorts} sort(s) au total.")

    # ====== Armes & Armure
    st.markdown("<h2>🛠️ Arme & Armure</h2>", unsafe_allow_html=True)
    arm_cols = st.columns(3)
    with arm_cols[0]:
        arme1 = st.selectbox("Arme principale", ["──"] + WEAPONS, key="arme1")
    with arm_cols[1]:
        arme2 = st.selectbox("Arme secondaire", ["──"] + WEAPONS, key="arme2")
    with arm_cols[2]:
        armure = st.selectbox("Type d'armure", ["──"] + ARMORS, key="armure")

    # ====== Équipement
    st.markdown("<h2>🎒 Équipement (8 objets)</h2>", unsafe_allow_html=True)
    eq_cols = st.columns(2)
    equipement: List[str] = []
    for c_idx, c in enumerate(eq_cols):
        for i in range(4):
            key = f"equip_{c_idx}_{i}"
            choix_eq = c.selectbox(f"Équipement {c_idx*4 + i + 1}", ["──"] + EQUIPMENT, key=key)
            if choix_eq == "Autre":
                autre = c.text_input("Précisez autre équipement", key=f"{key}_autre")
                if autre:
                    equipement.append(autre.strip())
            else:
                equipement.append(choix_eq)
    equipement = clean_choices(equipement)

    submitted = st.form_submit_button("Valider la création")

# =========================
# Validation (sans génération JSON)
# =========================
if submitted:
    errors = []

    if not (nom or "").strip():
        errors.append("Le nom du personnage est requis.")
    if remaining != 0:
        errors.append("La somme des caractéristiques doit être exactement 170%.")
    if len(selected_skills) != 4:
        errors.append("Tu dois sélectionner exactement 4 compétences uniques.")
    if alignment == "──":
        errors.append("Choisis un alignement.")
    if arme1 == "──":
        errors.append("Choisis une arme principale.")
    if armure == "──":
        errors.append("Choisis un type d'armure.")
    if (classe or "──") != "──" and num_sorts > 0 and len(sorts) < num_sorts:
        errors.append("Renseigne tous les sorts correspondant à ta classe.")

    if errors:
        for e in errors:
            st.error(e)
    else:
        st.success("✅ Personnage validé ! (sortie JSON supprimée comme demandé)")
