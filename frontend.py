import streamlit as st
from app import run_safer_pipeline
from chembl.resolver import search_drug_by_name, resolve_drug_by_chembl_id

st.set_page_config(page_title="S.A.F.E.R", layout="wide")

st.markdown(
    "<h1 style='color:#FFD700'>S.A.F.E.R</h1>",
    unsafe_allow_html=True
)

# ==================================================
# SESSION STATE
# ==================================================
if "selected_hit" not in st.session_state:
    st.session_state.selected_hit = None

if "search_results" not in st.session_state:
    st.session_state.search_results = []

# ==================================================
# SEARCH INPUT (NAME OR ChEMBL)
# ==================================================
st.subheader("Search by Drug Name or ChEMBL ID")

with st.form("drug_search_form"):
    query = st.text_input(
        "Enter drug name or ChEMBL ID",
        placeholder="Rosuvastatin, Aspirin, CHEMBL1496"
    )
    submitted = st.form_submit_button("Search")

# ==================================================
# HANDLE SEARCH
# ==================================================
if submitted and query:
    query = query.strip()

    # Reset previous state
    st.session_state.selected_hit = None
    st.session_state.search_results = []

    # -------------------------------
    # Case 1: Direct ChEMBL ID
    # -------------------------------
    if query.upper().startswith("CHEMBL"):
        with st.spinner("Resolving ChEMBL ID..."):
            try:
                drug = resolve_drug_by_chembl_id(query.upper())

                st.session_state.selected_hit = {
                    "name": drug["name"],
                    "chembl_id": query.upper(),
                    "description": drug.get("description")
                }

            except Exception as e:
                st.error(f"Failed to resolve ChEMBL ID: {e}")

    # -------------------------------
    # Case 2: Drug name search
    # -------------------------------
    else:
        with st.spinner("🔍 Checking Open Targets database..."):
            try:
                hits = search_drug_by_name(query)
            except Exception as e:
                st.error(str(e))
                hits = []

        if hits:
            st.session_state.search_results = hits
        else:
            st.warning("No matching drug found in Open Targets.")

# ==================================================
# MULTIPLE MATCH SELECTION
# ==================================================
if st.session_state.search_results:
    st.markdown("### Select the correct drug")

    for hit in st.session_state.search_results:
        if st.button(f"{hit['name']} ({hit['chembl_id']})"):
            st.session_state.selected_hit = hit
            st.session_state.search_results = []
            st.rerun()

# ==================================================
# DRUG SUMMARY CARD
# ==================================================
if st.session_state.selected_hit:
    hit = st.session_state.selected_hit

    st.success("Drug selected")

    st.markdown(
        f"""
        ## {hit['name'].upper()}
        **ChEMBL ID:** `{hit['chembl_id']}`

        {hit.get('description') or "_No description available from Open Targets._"}
        """
    )

    # ==================================================
    # RUN SAFER PIPELINE
    # ==================================================
    if st.button(f"Analyze {hit['name']}"):
        with st.spinner("Running SAFER pipeline..."):
            try:
                output = run_safer_pipeline(hit["chembl_id"])

                st.session_state["chembl_id"] = hit["chembl_id"]
                st.session_state["safer_output"] = output

                st.switch_page("pages/insights.py")

            except Exception as e:
                st.error(str(e))
