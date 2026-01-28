# app.py
"""
S.A.F.E.R – Safety-Aware Framework for Drug Repurposing
Application Orchestrator (Backend Entry Point)
"""

from chembl.validator import validate_chembl_id
from chembl.resolver import resolve_drug_by_chembl_id
from chembl.parser import parse_drug_response

from mechanism.fetcher import fetch_drug_mechanisms
from mechanism.normalizer import normalize_mechanisms

from indications.fetcher import fetch_drug_indications

from stage3.fetcher import fetch_target_disease_associations
from stage3.aggregator import aggregate_disease_associations
from stage3.filter import fetch_known_indications
from stage3.ranker import rank_diseases

from safety.fetcher import fetch_drug_safety_signals
from safety.normalizer import normalize_safety_signals
from safety.scorer import apply_safety_penalty


def run_safer_pipeline(chembl_id: str) -> dict:
    """
    Run the full SAFER pipeline for a given ChEMBL ID.
    """

    # -------------------------
    # Stage 1 – Drug identity
    # -------------------------
    validate_chembl_id(chembl_id)

    raw_drug = resolve_drug_by_chembl_id(chembl_id)
    drug = parse_drug_response(raw_drug)

    # -------------------------
    # Stage 2 – Mechanism & targets
    # -------------------------
    raw_mechanisms = fetch_drug_mechanisms(chembl_id)
    mechanisms = normalize_mechanisms(raw_mechanisms)

    targets = {
        t["id"]
        for moa in raw_mechanisms
        for t in moa.get("targets", [])
    }

    # -------------------------
    # Stage 2.5 – Approved indications (truth source)
    # -------------------------
    indications = fetch_drug_indications(chembl_id)

    # -------------------------
    # Stage 3 – Disease prioritization (repurposing)
    # -------------------------
    all_associations = []

    for target_id in targets:
        all_associations.extend(
            fetch_target_disease_associations(target_id)
        )

    aggregated = aggregate_disease_associations(all_associations)

    known_indications = fetch_known_indications(chembl_id)

    ranked_diseases = rank_diseases(
        aggregated,
        known_indications
    )

    # -------------------------
    # Stage 4 – Safety-aware scoring
    # -------------------------
    safety_signals = fetch_drug_safety_signals(chembl_id)
    safety_summary = normalize_safety_signals(safety_signals)

    safer_results = apply_safety_penalty(
        ranked_diseases,
        safety_summary
    )

    # -------------------------
    # Final output (frontend contract)
    # -------------------------
    return {
        "drug": drug,
        "mechanisms": mechanisms,
        "indications": indications,
        "safety_summary": safety_summary,
        "results": safer_results
    }


# -------------------------
# CLI execution (optional)
# -------------------------
if __name__ == "__main__":
    import pprint

    chembl_id = input("Enter ChEMBL ID (e.g., CHEMBL25): ").strip()

    try:
        output = run_safer_pipeline(chembl_id)
        pprint.pprint(output)
    except ValueError as e:
        print(f"\n❌ Error: {e}")
