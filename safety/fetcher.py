# ✅ safety/fetcher.py
import requests

# Open Targets v4 GraphQL Endpoint
OPEN_TARGETS_URL = "https://api.platform.opentargets.org/api/v4/graphql"

def fetch_drug_safety_signals(chembl_id: str) -> list[dict]:
    """
    Fetch drug safety signals (ADRs) using a direct GraphQL query.
    Aligned with Stage 4: Safety-Aware Scoring.
    """
    
    # Query using 'logLR' as confirmed by the Open Targets v4 schema
    query = """
    query DrugSafety($chemblId: String!) {
      drug(chemblId: $chemblId) {
        adverseEvents {
          rows {
            name
            count
            logLR
          }
        }
      }
    }
    """
    
    variables = {"chemblId": chembl_id}
    
    try:
        response = requests.post(
            OPEN_TARGETS_URL,
            json={"query": query, "variables": variables},
            timeout=15  # Standard timeout for network stability
        )
        
        # Explicit error reporting for 400/500 status codes
        if response.status_code != 200:
            print(f"DEBUG: API Error - {response.text}")
            
        response.raise_for_status()
        
    except requests.RequestException as e:
        raise ValueError(f"Failed to connect to Open Targets: {e}")

    payload = response.json()
    
    # Catch GraphQL-specific syntax or schema errors
    if "errors" in payload:
        error_msg = payload["errors"][0].get("message", "Unknown GraphQL error")
        raise ValueError(f"GraphQL Schema Error: {error_msg}")

    drug_data = payload.get("data", {}).get("drug")
    
    if not drug_data or not drug_data.get("adverseEvents"):
        return [] # Return empty list if no safety signals exist

    # Map API fields to the S.A.F.E.R internal format
    return [
        {
            "event": row.get("name"),
            "count": row.get("count"),
            "signal_strength": row.get("logLR")
        }
        for row in drug_data["adverseEvents"].get("rows", [])
    ]