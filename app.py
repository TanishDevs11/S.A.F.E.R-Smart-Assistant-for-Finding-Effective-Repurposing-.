from chembl.validator import validate_chembl_id
from chembl.resolver import resolve_drug_by_chembl_id
from chembl.parser import parse_drug_response


def get_drug_profile(chembl_id: str) -> dict:
    """
    End-to-end SAFER Stage-1 pipeline.
    """

    validated_id = validate_chembl_id(chembl_id)
    raw_drug = resolve_drug_by_chembl_id(validated_id)
    parsed_drug = parse_drug_response(raw_drug)

    return parsed_drug


if __name__ == "__main__":
    import sys

    if len(sys.argv) != 2:
        print("Usage: python app.py <CHEMBL_ID>")
        sys.exit(1)

    result = get_drug_profile(sys.argv[1])
    print(result)