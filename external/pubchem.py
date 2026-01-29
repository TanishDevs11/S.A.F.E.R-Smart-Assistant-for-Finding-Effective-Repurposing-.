import requests


def get_pubchem_description(drug_name: str) -> str | None:
    """
    Fetch a textual drug description from PubChem using PUG-REST + PUG-View.
    No API key required.
    """

    try:
        # Step 1: Resolve PubChem CID
        cid_url = (
            f"https://pubchem.ncbi.nlm.nih.gov/rest/pug/"
            f"compound/name/{drug_name}/cids/JSON"
        )
        cid_res = requests.get(cid_url, timeout=5)
        cid_res.raise_for_status()
        cid = cid_res.json()["IdentifierList"]["CID"][0]

        # Step 2: Fetch Record Description
        desc_url = (
            f"https://pubchem.ncbi.nlm.nih.gov/rest/pug_view/"
            f"data/compound/{cid}/JSON?heading=Record+Description"
        )
        desc_res = requests.get(desc_url, timeout=5)
        desc_res.raise_for_status()

        record = desc_res.json()["Record"]
        sections = record.get("Section", [])

        for section in sections:
            for info in section.get("Information", []):
                value = info.get("Value", {})
                strings = value.get("StringWithMarkup", [])
                if strings:
                    return strings[0]["String"]

        return None

    except Exception:
        return None
