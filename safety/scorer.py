# safety/scorer.py

from typing import List, Dict


def apply_safety_penalty(
    disease_rankings: List[Dict],
    safety_summary: Dict
) -> List[Dict]:
    """
    Re-score disease rankings based on drug safety risk.

    Args:
        disease_rankings: Output from Stage 3 prioritization
        safety_summary: Output from safety.normalizer

    Returns:
        List of diseases with adjusted SAFER scores
    """

    risk_level = safety_summary.get("risk_level", "LOW")

    # Explicit, interpretable penalty factors
    penalty_map = {
        "LOW": 1.0,
        "MEDIUM": 0.75,
        "HIGH": 0.5,
    }

    penalty = penalty_map.get(risk_level, 1.0)

    rescored = []

    for disease in disease_rankings:
        base_score = disease.get("association_score", 0)

        safer_score = round(base_score * penalty, 4)

        rescored.append({
            **disease,
            "safer_score": safer_score,
            "safety_risk": risk_level
        })

    # Sort by SAFER score
    rescored.sort(key=lambda x: x["safer_score"], reverse=True)

    return rescored
