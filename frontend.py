import streamlit as st
from app import run_safer_pipeline

st.set_page_config(page_title="Drug Repurposing Tool", layout="wide")

st.markdown("<h1 style='color:#FFD700'>Drug Repurposing Insights</h1>", unsafe_allow_html=True)

chembl_id = st.text_input(
    "Enter ChEMBL ID",
    placeholder="CHEMBL25, CHEMBL112, CHEMBL3137343"
)

if st.button("Search"):
    if not chembl_id:
        st.error("Please enter a ChEMBL ID")
    else:
        with st.spinner("Running SAFER pipeline..."):
            try:
                output = run_safer_pipeline(chembl_id)

                # Save everything for page 2
                st.session_state["chembl_id"] = chembl_id
                st.session_state["safer_output"] = output

                # Navigate to insights page
                st.switch_page("pages/insights.py")

            except Exception as e:
                st.error(str(e))
