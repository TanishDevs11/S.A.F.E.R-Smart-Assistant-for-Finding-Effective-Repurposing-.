# app.py
"""
S.A.F.E.R – Safety-Aware Framework for Drug Repurposing
Application Orchestrator (Backend Entry Point)
"""

from chembl.validator import validate_chembl_id
from chembl.resolver import resolve_drug_by_chembl_id
from chembl.parser import parse_drug_response

from mechanism.fetcher import fetch_drug_mechanisms

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
    mechanisms = fetch_drug_mechanisms(chembl_id)

    targets = set()
    for moa in mechanisms:
        for t in moa.get("targets", []):
            targets.add(t["id"])

    # -------------------------
        # -------------------------
    # Stage 3 – Disease prioritization
    # -------------------------
    all_associations = []

    for target_id in targets:
        associations = fetch_target_disease_associations(target_id)
        all_associations.extend(associations)

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
    # Final output
    # -------------------------
    return {
        "drug": drug,
        "safety_summary": safety_summary,
        "results": safer_results
    }


# Allow CLI-style execution
if __name__ == "__main__":
    import pprint

    chembl_id = input("Enter ChEMBL ID (e.g., CHEMBL25): ").strip()

    try:
        output = run_safer_pipeline(chembl_id)
        pprint.pprint(output)
    except ValueError as e:
        print(f"\n❌ Error: {e}")
