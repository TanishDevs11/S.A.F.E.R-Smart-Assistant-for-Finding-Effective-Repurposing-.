import json
import numpy as np


def load_pae_matrix(pae_json_path: str) -> np.ndarray:
    """
    Load AlphaFold Predicted Aligned Error (PAE) matrix.

    Supports both legacy and current AlphaFold JSON schemas.

    Args:
        pae_json_path (str): Path to AlphaFold PAE JSON file

    Returns:
        np.ndarray: NxN PAE matrix (Å)
    """

    with open(pae_json_path, "r") as f:
        data = json.load(f)

    # -------- Schema 1: Standard AlphaFold DB --------
    if "predicted_aligned_error" in data:
        pae = data["predicted_aligned_error"]

    # -------- Schema 2: Multi-model AlphaFold --------
    elif "pae" in data and isinstance(data["pae"], list):
        pae = data["pae"][0].get("predicted_aligned_error")

    else:
        raise ValueError(
            "Invalid AlphaFold PAE JSON format: "
            "expected 'predicted_aligned_error'"
        )

    pae_matrix = np.array(pae)

    if pae_matrix.ndim != 2:
        raise ValueError("PAE matrix is not 2-dimensional")

    return pae_matrix
