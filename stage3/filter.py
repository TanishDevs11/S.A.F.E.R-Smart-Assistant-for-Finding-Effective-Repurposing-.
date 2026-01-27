import requests
from typing import List, Dict

OPEN_TARGETS_GRAPHQL_URL = "https://api.platform.opentargets.org/api/v4/graphql"


def fetch_known_indications(chembl_id: str) -> set:
    """
    Fetch known disease indications for a drug from Open Targets.

    Args:
        chembl_id (str): Validated ChEMBL ID

    Returns:
        set[str]: Set of disease IDs (EFO / MONDO)
    """

    query = """
    query DrugIndications($chemblId: String!) {
      drug(chemblId: $chemblId) {
        indications {
          rows {
            disease {
              id
            }
          }
        }
      }
    }
    """

    variables = {"chemblId": chembl_id}

    response = requests.post(
        OPEN_TARGETS_GRAPHQL_URL,
        json={"query": query, "variables": variables},
        timeout=15,
    )

    if response.status_code != 200:
        raise ValueError(
            f"Open Targets API returned status code {response.status_code}"
        )

    payload = response.json()

    if "errors" in payload:
        raise ValueError(payload["errors"][0]["message"])

    drug = payload.get("data", {}).get("drug")

    if drug is None:
        return set()

    rows = drug.get("indications", {}).get("rows", [])

    known_diseases = set()
    for row in rows:
        disease = row.get("disease")
        if disease and disease.get("id"):
            known_diseases.add(disease["id"])

    return known_diseases


def label_known_indications(
    aggregated_diseases: List[Dict],
    chembl_id: str
) -> List[Dict]:
    """
    Label aggregated diseases as known indications or repurposing candidates.

    Args:
        aggregated_diseases (list): Output from Stage 3.2
        chembl_id (str): Drug ChEMBL ID

    Returns:
        list[dict]: Diseases with status field added
    """

    known_indications = fetch_known_indications(chembl_id)

    labeled = []
    for disease in aggregated_diseases:
        disease_id = disease.get("disease_id")

        status = (
            "known_indication"
            if disease_id in known_indications
            else "repurposing_candidate"
        )

        labeled.append(
            {
                **disease,
                "status": status
            }
        )

    return labeled
