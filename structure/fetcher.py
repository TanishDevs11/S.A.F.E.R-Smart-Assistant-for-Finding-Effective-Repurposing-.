import os
import json
import requests
from typing import Tuple, Optional

ALPHAFOLD_BASE_URL = "https://alphafold.ebi.ac.uk/files"

PDB_DIR = "structure/pdbs"
PAE_DIR = "structure/pae"

os.makedirs(PDB_DIR, exist_ok=True)
os.makedirs(PAE_DIR, exist_ok=True)


def fetch_alphafold_assets(uniprot_id: str) -> Tuple[str, Optional[str]]:
    """
    Fetch AlphaFold structural assets for a UniProt protein.

    Strategy:
    1️⃣ Prefer monomeric PDB model v6
    2️⃣ Fallback to monomeric PDB model v4
    3️⃣ Fetch PAE JSON v4 if available (OPTIONAL)

    Notes:
    - AlphaFold models are monomeric predictions.
    - They may not represent biological assemblies, complexes,
      membrane environments, or ligand-bound states.
    - PAE reflects structural confidence, NOT binding affinity.

    Args:
        uniprot_id (str): UniProt accession (e.g., Q9Y6K9)

    Returns:
        Tuple[str, Optional[str]]:
            - Path to AlphaFold PDB file
            - Path to AlphaFold PAE JSON file (or None if unavailable)
    """

    uniprot_id = uniprot_id.upper().strip()

    # -----------------------------
    # File names
    # -----------------------------
    pdb_v6_name = f"AF-{uniprot_id}-F1-model_v6.pdb"
    pdb_v4_name = f"AF-{uniprot_id}-F1-model_v4.pdb"
    pae_v4_name = f"AF-{uniprot_id}-F1-predicted_aligned_error_v4.json"

    pdb_v6_path = os.path.join(PDB_DIR, pdb_v6_name)
    pdb_v4_path = os.path.join(PDB_DIR, pdb_v4_name)
    pae_path = os.path.join(PAE_DIR, pae_v4_name)

    # ==================================================
    # 1️⃣ / 2️⃣ FETCH PDB (v6 → v4 fallback)
    # ==================================================
    pdb_path = None

    if os.path.exists(pdb_v6_path):
        pdb_path = pdb_v6_path

    elif os.path.exists(pdb_v4_path):
        pdb_path = pdb_v4_path

    else:
        # Try v6 first
        url_v6 = f"{ALPHAFOLD_BASE_URL}/{pdb_v6_name}"
        r = requests.get(url_v6, timeout=15)

        if r.status_code == 200:
            with open(pdb_v6_path, "wb") as f:
                f.write(r.content)
            pdb_path = pdb_v6_path

        else:
            # Fallback to v4
            url_v4 = f"{ALPHAFOLD_BASE_URL}/{pdb_v4_name}"
            r = requests.get(url_v4, timeout=15)

            if r.status_code == 200:
                with open(pdb_v4_path, "wb") as f:
                    f.write(r.content)
                pdb_path = pdb_v4_path
            else:
                raise ValueError(
                    f"No AlphaFold monomeric structure available for UniProt ID {uniprot_id}. "
                    "Protein may be membrane-bound, multi-chain, disordered, or unsupported."
                )

    # ==================================================
    # 3️⃣ FETCH PAE JSON (OPTIONAL — DO NOT CRASH)
    # ==================================================
    pae_available = True

    if not os.path.exists(pae_path):
        pae_url = f"{ALPHAFOLD_BASE_URL}/{pae_v4_name}"
        r = requests.get(pae_url, timeout=15)

        if r.status_code == 200:
            with open(pae_path, "w") as f:
                json.dump(r.json(), f)
        else:
            pae_available = False

    return pdb_path, (pae_path if pae_available else None)
