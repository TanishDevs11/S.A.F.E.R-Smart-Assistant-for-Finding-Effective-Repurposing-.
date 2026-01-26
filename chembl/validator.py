import re

CHEMBL_REGEX = re.compile(r"^CHEMBL[0-9]+$")

def validate_chembl_id(input_id: str) -> str:
    """
    Validates that the input ID matches the ChEMBL ID format.

    Args:
        input_id: The ID string to validate

    Returns:
        The validated ChEMBL ID string

    Raises:
        ValueError: If the input does not match the pattern CHEMBL[0-9]+
    """
    if not isinstance(input_id, str):
        raise ValueError("ChEMBL ID must be a string.")

    if not CHEMBL_REGEX.match(input_id):
        raise ValueError(
            f"Invalid ChEMBL ID format: '{input_id}'. Expected format: CHEMBL followed by digits (e.g. CHEMBL25)."
        )

    return input_id
