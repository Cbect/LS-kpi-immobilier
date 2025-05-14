import datetime
import streamlit as st

st.set_page_config(page_title="Dashboard KPI Immobilier", layout="centered")

st.title("📊 Dashboard – KPIs Locatifs")
st.markdown(
    """Ce tableau de bord calcule automatiquement :
    1. **Taux de vacance locative (TVL)**
    2. **Cash‑flow net mensuel (CFN)**
    3. **Rendement net annuel**
    4. **Compte à rebours DPE (mois restants)**

    Renseignez vos données dans la barre latérale 👉 pour obtenir les résultats en temps réel.
    """
)

# ───────────────────────── SIDEBAR ─────────────────────────

st.sidebar.header("Paramètres du bien")

# Revenus
loyer_mensuel = st.sidebar.number_input(
    "Loyer mensuel encaissé (€)", min_value=0.0, value=650.0, step=50.0, format="%.2f"
)
jours_vacants = st.sidebar.number_input(
    "Jours de vacance sur 12 mois (jours)", min_value=0, max_value=365, value=42, step=1
)

st.sidebar.markdown("---")

# Charges mensuelles (non récupérables)
charges_non_recup_mensuelles = st.sidebar.number_input(
    "Charges non récupérables mensuelles (€)", min_value=0.0, value=60.0, step=10.0, format="%.2f"
)

# Charges annuelles
st.sidebar.subheader("Charges annuelles")
taxe_fonciere = st.sidebar.number_input(
    "Taxe foncière (€)", min_value=0.0, value=800.0, step=50.0, format="%.2f"
)
assurance_pno = st.sidebar.number_input(
    "Assurance PNO (€)", min_value=0.0, value=120.0, step=10.0, format="%.2f"
)
travaux_annuels = st.sidebar.number_input(
    "Travaux / entretien (€)", min_value=0.0, value=500.0, step=50.0, format="%.2f"
)
interets_emprunt = st.sidebar.number_input(
    "Intérêts d'emprunt (€)", min_value=0.0, value=1500.0, step=100.0, format="%.2f"
)

st.sidebar.markdown("---")

# Coût d'acquisition
cout_acquisition = st.sidebar.number_input(
    "Coût total d'acquisition (€)", min_value=0.0, value=120000.0, step=1000.0, format="%.0f"
)

st.sidebar.markdown("---")

# DPE countdown
st.sidebar.subheader("⏳ Compte à rebours DPE")
dpe_date_limite = st.sidebar.date_input(
    "Date limite DPE", value=datetime.date(2028, 1, 1)
)

# ───────────────────────── CALCULS ─────────────────────────

# KPI 1 – TVL
TVL = (jours_vacants / 365) * 100  # en %
tvl_seuil = 10.0  # %

# KPI 2 – CFN
total_loyer_annuel = loyer_mensuel * 12
charges_non_recup_annuelles = charges_non_recup_mensuelles * 12
charges_annuelles_total = (
    charges_non_recup_annuelles
    + taxe_fonciere
    + assurance_pno
    + travaux_annuels
    + interets_emprunt
)
CFN = (total_loyer_annuel - charges_annuelles_total) / 12

# KPI 3 – Rendement net
rendement_net = ((total_loyer_annuel - charges_annuelles_total) / cout_acquisition) * 100

# KPI 4 – DPE countdown (mois)
aujourd_hui = datetime.date.today()
mois_left = (dpe_date_limite.year - aujourd_hui.year) * 12 + (dpe_date_limite.month - aujourd_hui.month)
if dpe_date_limite.day < aujourd_hui.day:
    mois_left -= 1

# ───────────────────────── AFFICHAGE ─────────────────────────

col1, col2 = st.columns(2)

with col1:
    st.metric(
        label="Taux de vacance locative (TVL)",
        value=f"{TVL:.1f} %",
        delta="🔺" if TVL > tvl_seuil else "✅"
    )
    st.metric(
        label="Cash‑flow net mensuel (CFN)",
        value=f"{CFN:,.0f} €",
        delta="Positif" if CFN >= 0 else "Négatif"
    )

with col2:
    st.metric(
        label="Rendement net annuel",
        value=f"{rendement_net:.2f} %"
    )
    st.metric(
        label="⏳ Compte à rebours DPE",
        value=f"{mois_left} mois",
        delta="En retard" if mois_left < 0 else "OK"
    )

# Détails
with st.expander("🔍 Détails du calcul"):
    st.write("### Données annuelles")
    st.write(
        {
            "Loyer annuel (€)": f"{total_loyer_annuel:,.0f}",
            "Charges annuelles (€)": f"{charges_annuelles_total:,.0f}",
            "Vacance (jours)": jours_vacants,
            "Mois restants DPE": mois_left,
        }
    )
    st.write("### Formules synthétiques")
    st.code(
        """
# TVL (%) = (jours_vacants / 365) * 100
# CFN (€) = (loyer_annuel – charges_annuelles_total) / 12
# Rendement net (%) = (loyer_annuel – charges_annuelles_total) / coût_acquisition × 100
# Mois restants DPE = diff_ym(date_limite, aujourd'hui)
        """,
        language="python",
    )

st.markdown("---")
st.caption("© 2025 – Dashboard généré par ChatGPT. Utilisation libre.")
