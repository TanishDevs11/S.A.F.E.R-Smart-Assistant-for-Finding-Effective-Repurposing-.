def map_targets_from_mechanisms(mechanisms: list[dict]) -> list[dict]:
    """
    Canonicalize drug targets from raw mechanism-of-action data.

    Args:
        mechanisms (list[dict]): Raw MoA rows from Stage 2.1

    Returns:
        list[dict]: Canonical target objects
    """

    canonical_targets = []

    for row in mechanisms:
        mechanism = row.get("mechanismOfAction")
        action_type = row.get("actionType")
        targets = row.get("targets", [])

        for target in targets:
            ensembl_id = target.get("id")
            gene_symbol = target.get("approvedSymbol")

            # Enforce human Ensembl gene targets only
            if not ensembl_id or not ensembl_id.startswith("ENSG"):
                continue

            if not gene_symbol:
                continue

            canonical_targets.append(
                {
                    "ensembl_id": ensembl_id,
                    "gene_symbol": gene_symbol,
                    "action_type": action_type,
                    "mechanism": mechanism,
                }
            )

    if not canonical_targets:
        raise ValueError("No valid gene targets could be canonicalized")

    return canonical_targets
