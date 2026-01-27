# ✅ mechanism/fetcher.py (UPDATED & LOCKED)

import requests

# Open Targets GraphQL endpoint
OPEN_TARGETS_GRAPHQL_URL = "https://api.platform.opentargets.org/api/v4/graphql"

def fetch_drug_mechanisms(chembl_id: str) -> list[dict]:
    """
    Fetch raw mechanism-of-action data for a drug from Open Targets using the v4 schema.
    This implementation accounts for the 'rows' pagination and plural 'targets' field.

    Args:
        chembl_id (str): Validated ChEMBL ID from Stage 1.

    Returns:
        list[dict]: A list of mechanism rows containing action types and target metadata.

    Raises:
        ValueError: If the API returns a 400/500 error, GraphQL errors, or if the drug is not found.
    """

    # Corrected GraphQL query to match Open Targets v4+ schema
    query = """
    query DrugMechanisms($chemblId: String!) {
      drug(chemblId: $chemblId) {
        mechanismsOfAction {
          rows {                  # Required for v4 pagination
            mechanismOfAction
            actionType
            targets {             # Correct plural field name
              id
              approvedSymbol
            }
          }
        }
      }
    }
    """

    variables = {"chemblId": chembl_id}

    try:
        response = requests.post(
            OPEN_TARGETS_GRAPHQL_URL,
            json={"query": query, "variables": variables},
            timeout=15,  # Standard timeout
        )
    except requests.RequestException as e:
        raise ValueError(f"Failed to connect to Open Targets API: {e}")

    # Handle HTTP-level errors
    if response.status_code != 200:
        raise ValueError(
            f"Open Targets API returned status code {response.status_code}: {response.text}"
        )

    payload = response.json()

    # Handle GraphQL-specific errors (this prevents silent 400 failures)
    if "errors" in payload:
        error_msg = payload["errors"][0].get("message", "Unknown GraphQL error")
        raise ValueError(f"GraphQL Query Error: {error_msg}")

    drug = payload.get("data", {}).get("drug")

    if drug is None:
        raise ValueError(f"Drug {chembl_id} not found in Open Targets database")

    # Access the nested 'rows' list
    moa_data = drug.get("mechanismsOfAction", {})
    mechanisms = moa_data.get("rows", [])

    if not mechanisms:
        raise ValueError(
            f"No mechanism-of-action data found for drug {chembl_id}"
        )

    return mechanisms