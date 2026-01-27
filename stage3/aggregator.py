from collections import defaultdict
from typing import List, Dict


def aggregate_disease_associations(associations: List[Dict]) -> List[Dict]:
    """
    Aggregate disease association scores across all targets.

    Args:
        associations: List of target-disease association records

    Returns:
        List of diseases with aggregated association scores
    """

    disease_scores = defaultdict(list)

    for record in associations:
        disease_id = record.get("disease_id")
        disease_name = record.get("disease_name")
        score = record.get("association_score", 0)

        if disease_id:
            disease_scores[disease_id].append(
                {
                    "disease_name": disease_name,
                    "score": score
                }
            )

    aggregated = []

    for disease_id, entries in disease_scores.items():
        scores = [e["score"] for e in entries]
        disease_name = entries[0]["disease_name"]

        aggregated.append(
            {
                "disease_id": disease_id,
                "disease_name": disease_name,
                "association_score": round(sum(scores) / len(scores), 4)
            }
        )

    return aggregated
