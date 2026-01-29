import streamlit as st
import pandas as pd
import plotly.express as px
from collections import defaultdict

# External + structural utilities
from external.pubchem import get_pubchem_description
from structure.uniprot_resolver import gene_to_uniprot
from structure.fetcher import fetch_alphafold_assets
from structure.processor import load_pae_matrix
from structure.plotter import plot_pae_map


# ==================================================
# PAGE CONFIG
# ==================================================
st.set_page_config(page_title="Drug Insights", layout="wide")


# ==================================================
# CSS
# ==================================================
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


# ==================================================
# GUARD CLAUSE
# ==================================================
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


# ==================================================
# HEADER
# ==================================================
st.markdown(
    f"<h1 style='color:#FFD700'>{drug['drug_name']} – Drug Repurposing Insights</h1>",
    unsafe_allow_html=True
)


# ==================================================
# ABOUT THE DRUG
# ==================================================
st.subheader("About the Drug")

description = drug.get("description")

if not description:
    with st.spinner("Fetching description from PubChem..."):
        description = get_pubchem_description(drug["drug_name"])

if not description:
    description = (
        f"{drug['drug_name']} is an established therapeutic agent. "
        "S.A.F.E.R evaluates this drug beyond its approved indications by "
        "integrating mechanism-of-action data, disease associations, and "
        "real-world safety signals to explore potential repurposing opportunities."
    )

st.markdown(description)

if drug.get("maximumClinicalTrialPhase"):
    st.caption(
        f"Lifecycle status: Approved (Phase {drug['maximumClinicalTrialPhase']})"
    )


# ==================================================
# BLACK BOX WARNING
# ==================================================
if safety.get("risk_level") == "HIGH":
    st.error(
        "⚠️ Black Box Warning: High-risk adverse events detected "
        "(e.g., severe bleeding, organ toxicity)."
    )


# ==================================================
# MECHANISM OF ACTION
# ==================================================
st.subheader("Mechanism of Action")

if not mechanisms:
    st.info("No mechanism-of-action data available.")
else:
    for moa in mechanisms:
        targets = ", ".join(moa.get("targets", [])) or "Unknown target"
        st.markdown(
            f"• **{moa['mechanism']}** ({moa['action_type']}) → {targets}"
        )


# ==================================================
# APPROVED & INVESTIGATIONAL INDICATIONS
# ==================================================
st.subheader("Approved & Investigational Indications")

# ---------------- APPROVED ----------------
st.markdown("### Approved")

cols = st.columns(4)
for i, ind in enumerate(approved_inds[:3]):
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

if len(approved_inds) > 3:
    with cols[3]:
        with st.expander(f"▼ Other approved ({len(approved_inds) - 3})"):
            for ind in approved_inds[3:]:
                areas = ", ".join(ind.get("areas", []))
                st.markdown(f"- **{ind['name'].title()}** — {areas}")

# ---------------- INVESTIGATIONAL ----------------
st.markdown("### Investigational")

phase_groups = defaultdict(list)
for ind in investigational_inds:
    phase_groups[ind["phase"]].append(ind)

for phase in sorted(phase_groups.keys(), reverse=True):
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

if events:
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
else:
    st.info("No high-risk safety signals available.")


# ==================================================
# STRUCTURAL PROTOTYPE MODE (ALPHAFOLD PAE)
# ==================================================
st.divider()
st.subheader("🧬 Structural Prototype Mode")

structural_mode = st.checkbox(
    "Enable Structural Confidence Map (AlphaFold PAE)",
    help="Displays AlphaFold Predicted Aligned Error (PAE) for educational use",
    key="structural_mode"
)

# ---------------- TARGET CONTEXT ----------------
gene_symbol = None
if mechanisms and mechanisms[0].get("targets"):
    gene_symbol = mechanisms[0]["targets"][0]
    st.caption(f"Detected target gene: **{gene_symbol}**")
else:
    st.warning("No protein target available for structural analysis.")

# ---------------- STRUCTURAL EXECUTION ----------------
if structural_mode and gene_symbol:
    try:
        with st.spinner("Resolving UniProt ID..."):
            uniprot_id = gene_to_uniprot(gene_symbol)

        with st.spinner("Fetching AlphaFold structural assets..."):
            _, pae_path = fetch_alphafold_assets(uniprot_id)

        with st.spinner("Rendering structural confidence map..."):
            pae_matrix = load_pae_matrix(pae_path)

        fig = plot_pae_map(
            pae_matrix,
            title=f"Predicted Aligned Error (PAE) – {gene_symbol} ({uniprot_id})"
        )

        st.plotly_chart(fig, use_container_width=True)

        st.caption(
            "⚠️ Educational / Prototype Mode: "
            "PAE reflects AlphaFold-predicted structural confidence "
            "(expected residue position error in Å). "
            "This does NOT represent drug binding affinity or dynamics."
        )

    except Exception as e:
        st.error(f"Structural analysis failed: {e}")

elif not structural_mode:
    st.info(
        "Enable the checkbox above to explore AlphaFold structural confidence."
    )
