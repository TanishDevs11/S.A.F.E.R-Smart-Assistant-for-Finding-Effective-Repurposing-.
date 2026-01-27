import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(page_title="Drug Insights", layout="wide")

# --------------------
# Guard clause
# --------------------
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

# --------------------
# HEADER
# --------------------
st.markdown(
    f"<h1 style='color:#FFD700'>{drug['drug_name']} – Drug Repurposing Insights</h1>",
    unsafe_allow_html=True
)

# --------------------
# BLACK BOX WARNING
# --------------------
if safety["risk_level"] == "HIGH":
    st.error(
        "⚠️ **Black Box Warning**: High-risk adverse events detected "
        "(e.g. gastrointestinal bleeding, hemorrhage)."
    )

# --------------------
# MECHANISM OF ACTION
# --------------------
st.subheader("Mechanism of Action")

if not mechanisms:
    st.info("No mechanism-of-action data available for this drug.")
else:
    for moa in mechanisms:
        targets = ", ".join(moa["targets"]) if moa["targets"] else "Unknown target"
        st.markdown(
            f"• **{moa['mechanism']}** ({moa['action_type']}) → {targets}"
        )

# --------------------
# APPROVED & INVESTIGATIONAL INDICATIONS (✅ FIXED)
# --------------------
st.subheader("Approved & Investigational Indications")

cols = st.columns(5)

# Approved
for i, ind in enumerate(approved_inds[:4]):
    cols[i].success(f"{ind}\n\nApproved")

# Investigational (if present)
if investigational_inds:
    cols[-1].info(f"{investigational_inds[0]}\n\nInvestigational")
else:
    cols[-1].warning("No investigational indications")

# --------------------
# REPURPOSING OPPORTUNITIES
# --------------------
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

# --------------------
# SAFETY INSIGHTS – CHARTS
# --------------------
st.subheader("Safety Insights")

events = safety["high_risk_events"][:5]
counts = list(range(len(events), 0, -1))

fig1 = px.bar(
    x=counts,
    y=events,
    orientation="h",
    title="Pharmacovigilance by Drug",
    labels={"x": "Relative Signal Strength", "y": "Adverse Event"}
)
st.plotly_chart(fig1, use_container_width=True)

# Radar chart (illustrative but data-driven later)
radar_df = pd.DataFrame({
    "Target Family": ["Immune", "Inflammatory", "Cardiovascular", "Metabolic", "Other"],
    "Risk": [5, 3, 2, 1, 1]
})

fig2 = px.line_polar(
    radar_df,
    r="Risk",
    theta="Target Family",
    line_close=True,
    title="Pharmacovigilance by Target Family"
)
st.plotly_chart(fig2, use_container_width=True)
