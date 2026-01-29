import streamlit as st
import pandas as pd
import plotly.express as px
from collections import defaultdict
from external.pubchem import get_pubchem_description

st.set_page_config(page_title="Drug Insights", layout="wide")

# --------------------------------------------------
# CSS
# --------------------------------------------------
st.markdown("""
<style>
.indication-card {
    min-width: 220px;
    padding: 1rem;
    border-radius: 10px;
    font-weight: 500;
}
.approved {
    background-color: #123d2a;
    color: #4cff9b;
}
.investigational {
    background-color: #1e2f44;
    color: #4da3ff;
}
</style>
""", unsafe_allow_html=True)

# --------------------------------------------------
# Guard clause
# --------------------------------------------------
if "safer_output" not in st.session_state:
    st.error("Please search for a drug first.")
    st.stop()

data = st.session_state["safer_output"]

drug = data["drug"]
results = data["results"]
safety = data["safety_summary"]
mechanisms = data.get("mechanisms", [])
indications = data.get("indications", {})

approved_inds = indications.get("approved", [])
investigational_inds = indications.get("investigational", [])

# --------------------------------------------------
# HEADER
# --------------------------------------------------
st.markdown(
    f"<h1 style='color:#FFD700'>{drug['drug_name']} – Drug Repurposing Insights</h1>",
    unsafe_allow_html=True
)

# ==================================================
# ABOUT THE DRUG (FIXED – NO GENERIC PHASE TEXT)
# ==================================================
st.subheader("About the Drug")

description = drug.get("description")

# Fallback → PubChem
if not description:
    with st.spinner("Fetching description from PubChem..."):
        description = get_pubchem_description(drug["drug_name"])

# Final fallback (context-aware, NOT misleading)
if not description:
    description = (
        f"{drug['drug_name']} is an established therapeutic agent. "
        "S.A.F.E.R evaluates this drug beyond its approved indications by "
        "integrating mechanism-of-action data, disease associations, and "
        "real-world safety signals to explore potential repurposing opportunities."
    )

st.markdown(description)

# Optional subtle lifecycle info (NOT headline text)
if drug.get("maximumClinicalTrialPhase"):
    st.caption(
        f"Lifecycle status: Approved (Phase {drug['maximumClinicalTrialPhase']})"
    )

# --------------------------------------------------
# BLACK BOX WARNING
# --------------------------------------------------
if safety.get("risk_level") == "HIGH":
    st.error(
        "⚠️ Black Box Warning: High-risk adverse events detected "
        "(e.g. gastrointestinal bleeding, hemorrhage)."
    )

# --------------------------------------------------
# MECHANISM OF ACTION
# --------------------------------------------------
st.subheader("Mechanism of Action")

if not mechanisms:
    st.info("No mechanism-of-action data available.")
else:
    for moa in mechanisms:
        targets = ", ".join(moa["targets"]) if moa["targets"] else "Unknown target"
        st.markdown(
            f"• **{moa['mechanism']}** ({moa['action_type']}) → {targets}"
        )

# ==================================================
# APPROVED & INVESTIGATIONAL INDICATIONS
# ==================================================
st.subheader("Approved & Investigational Indications")

# ---------------- APPROVED ----------------
st.markdown("### Approved")

approved_main = approved_inds[:3]
approved_extra = approved_inds[3:]

cols = st.columns(4)

for i in range(3):
    if i < len(approved_main):
        ind = approved_main[i]
        areas = ", ".join(ind.get("areas", []))

        cols[i].markdown(
            f"""
            <div class="indication-card approved">
                <b>{ind['name'].title()}</b><br>
                <small>{areas}</small><br><br>
                <small>Status: Approved</small>
            </div>
            """,
            unsafe_allow_html=True
        )
    else:
        cols[i].markdown("&nbsp;", unsafe_allow_html=True)

if approved_extra:
    with cols[3]:
        with st.expander(f"▼ Other approved ({len(approved_extra)})"):
            for ind in approved_extra:
                areas = ", ".join(ind.get("areas", []))
                st.markdown(f"- **{ind['name'].title()}** — {areas}")

# ---------------- INVESTIGATIONAL ----------------
st.markdown("### Investigational")

investigational_main = investigational_inds[:1]
investigational_extra = investigational_inds[1:]

phase_groups = defaultdict(list)
for ind in investigational_extra:
    phase_groups[ind["phase"]].append(ind)

sorted_phases = sorted(phase_groups.keys(), reverse=True)

cols = st.columns(4)

if investigational_main:
    ind = investigational_main[0]
    areas = ", ".join(ind.get("areas", []))

    cols[0].markdown(
        f"""
        <div class="indication-card investigational">
            <b>{ind['name'].title()}</b><br>
            <small>{areas}</small><br><br>
            <small>Status: Phase {ind['phase']}</small>
        </div>
        """,
        unsafe_allow_html=True
    )

if investigational_extra:
    with cols[3]:
        with st.expander(f"▼ Other investigational ({len(investigational_extra)})"):
            for phase in sorted_phases:
                with st.expander(f"Phase {phase}"):
                    for ind in phase_groups[phase]:
                        areas = ", ".join(ind.get("areas", []))
                        st.markdown(
                            f"- **{ind['name'].title()}**  \n<small>{areas}</small>",
                            unsafe_allow_html=True
                        )

# ==================================================
# REPURPOSING OPPORTUNITIES
# ==================================================
st.subheader("Repurposing Opportunities")

df = pd.DataFrame(results)
df["confidence"] = (df["safer_score"] * 100).round(1)

for _, row in df.head(5).iterrows():
    st.markdown(
        f"""
        **{row['disease_name']}**  
        Association score: {row['association_score']}  
        **{row['confidence']}% confidence**
        """
    )
    st.progress(row["confidence"] / 100)

# ==================================================
# SAFETY INSIGHTS
# ==================================================
st.subheader("Safety Insights")

events = safety.get("high_risk_events", [])[:5]

if not events:
    st.info("No high-risk safety signals available.")
else:
    df_events = pd.DataFrame({
        "Adverse Event": events,
        "Relative Signal Strength": list(range(len(events), 0, -1))
    })

    fig1 = px.bar(
        df_events,
        x="Relative Signal Strength",
        y="Adverse Event",
        orientation="h",
        title="Pharmacovigilance by Drug"
    )

    st.plotly_chart(fig1, use_container_width=True)

# ==================================================
# TARGET FAMILY RADAR
# ==================================================
st.subheader("Pharmacovigilance by Target Family")

family_risk = data.get("family_risk", {})

if not family_risk:
    st.info("No target-family risk data available.")
else:
    radar_df = pd.DataFrame({
        "Target Family": list(family_risk.keys()),
        "Risk": list(family_risk.values())
    })

    fig2 = px.line_polar(
        radar_df,
        r="Risk",
        theta="Target Family",
        line_close=True,
        title="Safety Risk by Biological Target Family"
    )

    st.plotly_chart(fig2, use_container_width=True)
