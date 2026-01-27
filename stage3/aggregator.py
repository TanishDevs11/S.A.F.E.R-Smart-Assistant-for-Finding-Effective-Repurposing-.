from collections import defaultdict
from typing import List, Dict


def aggregate_disease_associations(
    target_disease_map: Dict[str, List[dict]]
) -> List[dict]:
    """
    Aggregate disease associations across multiple targets.

    Args:
        target_disease_map (dict):
            {
              "PTGS1": [
                  {"disease_id": str, "disease_name": str, "association_score": float},
                  ...
              ],
              "PTGS2": [
                  {...}
              ]
            }

    Returns:
        list[dict]: Aggregated disease list:
            [
              {
                "disease_id": str,
                "disease_name": str,
                "association_score": float,
                "supporting_targets": list[str]
              }
            ]
    """

    disease_index = defaultdict(
        lambda: {
            "disease_name": None,
            "association_score": 0.0,
            "supporting_targets": set(),
        }
    )

    for target_symbol, disease_list in target_disease_map.items():
        for entry in disease_list:
            disease_id = entry.get("disease_id")
            disease_name = entry.get("disease_name")
            score = entry.get("association_score")

            if disease_id is None or score is None:
                continue

            record = disease_index[disease_id]

            record["disease_name"] = disease_name
            record["association_score"] = max(
                record["association_score"], score
            )
            record["supporting_targets"].add(target_symbol)

    aggregated = []
    for disease_id, data in disease_index.items():
        aggregated.append(
            {
                "disease_id": disease_id,
                "disease_name": data["disease_name"],
                "association_score": data["association_score"],
                "supporting_targets": sorted(list(data["supporting_targets"])),
            }
        )

    return aggregated
