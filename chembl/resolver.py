import requests

OPEN_TARGETS_GRAPHQL_URL = "https://api.platform.opentargets.org/api/v4/graphql"


def resolve_drug_by_chembl_id(chembl_id: str) -> dict:
    """
    Resolve a drug entity from Open Targets using a validated ChEMBL ID.

    Args:
        chembl_id (str): A validated ChEMBL ID (e.g. CHEMBL25)

    Returns:
        dict: Raw drug metadata from Open Targets

    Raises:
        ValueError: If the drug is not found or the API call fails
    """

    query = """
    query DrugByChEMBL($chemblId: String!) {
      drug(chemblId: $chemblId) {
        id
        name
        drugType
        maximumClinicalTrialPhase
      }
    }
    """

    variables = {"chemblId": chembl_id}

    try:
        response = requests.post(
            OPEN_TARGETS_GRAPHQL_URL,
            json={"query": query, "variables": variables},
            timeout=15,
        )
    except requests.RequestException as e:
        raise ValueError(f"Failed to connect to Open Targets API: {e}")

    if response.status_code != 200:
        raise ValueError(
            f"Open Targets API returned status code {response.status_code}"
        )

    payload = response.json()
    drug = payload.get("data", {}).get("drug")

    if drug is None:
        raise ValueError(f"Drug with ChEMBL ID {chembl_id} not found.")

    return drug
