import requests

def gene_to_canonical_uniprot(gene_symbol: str, organism="9606"):
    """
    Resolve gene symbol to canonical reviewed UniProt accession (Swiss-Prot).
    """
    url = (
        "https://rest.uniprot.org/uniprotkb/search?"
        f"query=gene:{gene_symbol}+AND+organism_id:{organism}+AND+reviewed:true"
        "&fields=accession"
        "&format=json"
        "&size=1"
    )

    r = requests.get(url, timeout=15)
    r.raise_for_status()
    data = r.json()

    results = data.get("results", [])
    if not results:
        return None

    return results[0]["primaryAccession"]
