import requests

def fetch_pae_matrix(uniprot_id: str):
    """
    Fetch AlphaFold Predicted Aligned Error (PAE) matrix.
    """
    uniprot_id = uniprot_id.upper()
    url = (
        f"https://alphafold.ebi.ac.uk/files/"
        f"AF-{uniprot_id}-F1-predicted_aligned_error_v4.json"
    )

    r = requests.get(url, timeout=15)
    if r.status_code != 200:
        raise ValueError("PAE data not available for this protein")

    data = r.json()
    return data[0]["predicted_aligned_error"]
