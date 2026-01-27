def normalize_mechanisms(raw_mechanisms: list[dict]) -> list[dict]:
    """
    Convert raw Open Targets mechanism data into UI-friendly format.
    """

    normalized = []

    for moa in raw_mechanisms:
        targets = [
            t["approvedSymbol"]
            for t in moa.get("targets", [])
            if t.get("approvedSymbol")
        ]

        normalized.append({
            "mechanism": moa.get("mechanismOfAction"),
            "action_type": moa.get("actionType"),
            "targets": targets
        })

    return normalized

