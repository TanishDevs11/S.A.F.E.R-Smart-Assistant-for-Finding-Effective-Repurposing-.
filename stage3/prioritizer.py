# stage3/prioritizer.py

from stage3.fetcher import fetch_target_disease_associations
from stage3.filter import fetch_known_indications
from stage3.aggregator import aggregate_disease_associations
from stage3.ranker import rank_diseases


def prioritize_diseases(chembl_id: str) -> list[dict]:
    """
    Stage 3 public API:
    Drug (CHEMBL) → Targets → Diseases → Ranked disease list
    """

    # Step 1: Fetch raw target–disease associations
    associations = fetch_target_disease_associations(chembl_id)

    # Step 2: Fetch known indications for this drug
    known_indications = fetch_known_indications(chembl_id)

    # Step 3: Remove known indications (repurposing-only)
    filtered = [
        assoc for assoc in associations
        if assoc.get("disease_id") not in known_indications
    ]

    # Step 4: Aggregate evidence into disease scores
    aggregated = aggregate_disease_associations(filtered)


    # Step 5: Rank diseases by association strength
    ranked = rank_diseases(aggregated)

    return ranked
