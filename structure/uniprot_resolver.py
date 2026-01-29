import requests

UNIPROT_SEARCH_URL = "https://rest.uniprot.org/uniprotkb/search"


def gene_to_uniprot(gene_symbol: str, organism: str = "9606") -> str:
    """
    Resolve a human gene symbol to a UniProt ID.
    
    Args:
        gene_symbol: e.g. PTGS2
        organism: NCBI taxonomy ID (9606 = human)

    Returns:
        UniProt accession (e.g. P35354)

    Raises:
        ValueError if no mapping found
    """

    params = {
        "query": f"(gene:{gene_symbol}) AND (organism_id:{organism})",
        "format": "json",
        "fields": "accession",
        "size": 1
    }

    response = requests.get(UNIPROT_SEARCH_URL, params=params, timeout=15)

    if response.status_code != 200:
        raise ValueError("UniProt API error")

    data = response.json()

    results = data.get("results", [])
    if not results:
        raise ValueError(f"No UniProt entry found for gene {gene_symbol}")

    return results[0]["primaryAccession"]
