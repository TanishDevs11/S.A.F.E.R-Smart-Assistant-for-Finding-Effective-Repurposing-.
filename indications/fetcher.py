import requests

OPEN_TARGETS_URL = "https://api.platform.opentargets.org/api/v4/graphql"

def fetch_drug_indications(chembl_id: str) -> dict:
    """
    Fetch approved and investigational indications for a drug.
    """

    query = """
    query DrugIndications($chemblId: String!) {
      drug(chemblId: $chemblId) {
        indications {
          rows {
            disease {
              name
            }
            maxPhaseForIndication
          }
        }
      }
    }
    """

    variables = {"chemblId": chembl_id}

    response = requests.post(
        OPEN_TARGETS_URL,
        json={"query": query, "variables": variables},
        timeout=15
    )

    if response.status_code != 200:
        raise ValueError("Failed to fetch drug indications")

    payload = response.json()

    if "errors" in payload:
        raise ValueError(payload["errors"][0]["message"])

    rows = payload["data"]["drug"]["indications"]["rows"]

    approved = []
    investigational = []

    for r in rows:
        name = r["disease"]["name"]
        phase = r["maxPhaseForIndication"]

        if phase == 4:
            approved.append(name)
        else:
            investigational.append(name)

    return {
        "approved": approved,
        "investigational": investigational
    }
