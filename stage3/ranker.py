from typing import List, Dict


def rank_diseases(diseases: List[Dict]) -> List[Dict]:
    """
    Rank diseases by association score and number of supporting targets.

    Ranking order:
    1. Highest association_score first
    2. Highest number of supporting_targets second

    Args:
        diseases (list): Output from Stage 3.3

    Returns:
        list[dict]: Ranked disease list
    """

    return sorted(
        diseases,
        key=lambda d: (
            d.get("association_score", 0),
            len(d.get("supporting_targets", [])),
        ),
        reverse=True,
    )
