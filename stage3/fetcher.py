import requests

# Open Targets GraphQL endpoint (live, no dataset uploads)
OPEN_TARGETS_GRAPHQL_URL = "https://api.platform.opentargets.org/api/v4/graphql"


def fetch_target_disease_associations(ensembl_id: str) -> list[dict]:
    """
    Fetch direct target–disease associations for a given target
    using Open Targets (overall association score).

    Args:
        ensembl_id (str): Ensembl gene ID (e.g. ENSG00000073756)

    Returns:
        list[dict]: [
            {
              "disease_id": str,
              "disease_name": str,
              "association_score": float
            }
        ]

    Raises:
        ValueError: If API fails or no associations are found
    """

    query = """
    query TargetDiseases($ensemblId: String!) {
      target(ensemblId: $ensemblId) {
        associatedDiseases {
          rows {
            disease {
              id
              name
            }
            score
          }
        }
      }
    }
    """

    variables = {"ensemblId": ensembl_id}

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

    if "errors" in payload:
        raise ValueError(payload["errors"][0]["message"])

    target = payload.get("data", {}).get("target")

    if target is None:
        raise ValueError(f"Target {ensembl_id} not found")

    rows = target.get("associatedDiseases", {}).get("rows", [])

    if not rows:
        raise ValueError(
            f"No disease associations found for target {ensembl_id}"
        )

    results = []
    for row in rows:
        disease = row.get("disease")
        score = row.get("score")

        if disease and score is not None:
            results.append(
                {
                    "disease_id": disease.get("id"),
                    "disease_name": disease.get("name"),
                    "association_score": score,
                }
            )

    return results
