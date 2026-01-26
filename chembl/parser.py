def parse_drug_response(raw_drug: dict) -> dict:
    """
    Parse raw Open Targets drug data into SAFER canonical format.
    """

    if not isinstance(raw_drug, dict):
        raise ValueError("Raw drug response must be a dictionary")

    return {
        "chembl_id": raw_drug.get("id"),
        "drug_name": raw_drug.get("name"),
        "drug_type": raw_drug.get("drugType"),
        "clinical_status": (
            str(raw_drug["maximumClinicalTrialPhase"])
            if raw_drug.get("maximumClinicalTrialPhase") is not None
            else None
        ),
    }
