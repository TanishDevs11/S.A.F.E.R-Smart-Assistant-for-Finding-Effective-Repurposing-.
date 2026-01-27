from typing import List, Dict, Set


def rank_diseases(
    diseases: List[Dict],
    known_indications: Set[str]
) -> List[Dict]:
    """
    Rank diseases by association score, excluding known indications.

    Args:
        diseases: Aggregated disease associations
        known_indications: Set of disease IDs already indicated for the drug

    Returns:
        Ranked list of candidate repurposing diseases
    """

    # Filter out diseases already indicated
    filtered = [
        d for d in diseases
        if d.get("disease_id") not in known_indications
    ]

    # Sort by association score (descending)
    ranked = sorted(
        filtered,
        key=lambda x: x.get("association_score", 0),
        reverse=True
    )

    return ranked
