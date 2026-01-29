import requests

OPEN_TARGETS_GRAPHQL_URL = "https://api.platform.opentargets.org/api/v4/graphql"


# ======================================================
# Resolve drug by ChEMBL ID (USED BY app.py)
# ======================================================
def resolve_drug_by_chembl_id(chembl_id: str) -> dict:
    """
    Resolve drug metadata + description from Open Targets.
    """

    query = """
    query DrugByChEMBL($chemblId: String!) {
      drug(chemblId: $chemblId) {
        id
        name
        drugType
        maximumClinicalTrialPhase
        description
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

    if not drug:
        raise ValueError(f"Drug with ChEMBL ID {chembl_id} not found.")

    return drug


# ======================================================
# Search drug by NAME (USED BY frontend.py)
# ======================================================
def search_drug_by_name(name: str) -> list:
    """
    Search Open Targets for drugs by name.
    Returns a LIST of hits.
    """

    query = """
    query DrugSearch($name: String!) {
      search(queryString: $name, entityNames: ["drug"]) {
        hits {
          id
          name
          description
        }
      }
    }
    """

    variables = {"name": name}

    response = requests.post(
        OPEN_TARGETS_GRAPHQL_URL,
        json={"query": query, "variables": variables},
        timeout=15,
    )

    if response.status_code != 200:
        raise ValueError("Failed to search drugs in Open Targets")

    payload = response.json()

    hits = payload.get("data", {}).get("search", {}).get("hits", [])

    results = []
    for hit in hits:
        if hit.get("id", "").startswith("CHEMBL"):
            results.append({
                "name": hit.get("name"),
                "chembl_id": hit.get("id"),
                "description": hit.get("description")
            })

    return results
