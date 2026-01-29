import requests

OPEN_TARGETS_URL = "https://api.platform.opentargets.org/api/v4/graphql"


def fetch_drug_indications(chembl_id: str) -> dict:
    """
    Fetch approved and investigational indications for a drug
    with phase and disease area metadata.
    """

    query = """
    query DrugIndications($chemblId: String!) {
      drug(chemblId: $chemblId) {
        indications {
          rows {
            disease {
              name
              therapeuticAreas {
                name
              }
            }
            maxPhaseForIndication
          }
        }
      }
    }
    """

    response = requests.post(
        OPEN_TARGETS_URL,
        json={"query": query, "variables": {"chemblId": chembl_id}},
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

        # extract disease areas safely
        areas = [
            ta["name"]
            for ta in r["disease"].get("therapeuticAreas", [])
        ]

        record = {
            "name": name,
            "phase": phase,
            "areas": areas
        }

        if phase == 4:
            approved.append(record)
        else:
            investigational.append(record)

    return {
        "approved": approved,
        "investigational": investigational
    }
