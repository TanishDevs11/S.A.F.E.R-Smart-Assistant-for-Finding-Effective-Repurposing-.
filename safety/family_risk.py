# safety/family_risk.py

def compute_family_risk(families: set, safety_signals: list) -> dict:
    family_scores = {family: 0.0 for family in families}

    for signal in safety_signals:
        event = signal["event"].lower()
        strength = signal["signal_strength"]

        if "haemorrhage" in event or "bleeding" in event:
            if "Inflammatory" in family_scores:
                family_scores["Inflammatory"] += strength

        if "cardiac" in event or "heart" in event:
            if "Cardiovascular" in family_scores:
                family_scores["Cardiovascular"] += strength

        if "diabetes" in event or "glucose" in event:
            if "Metabolic" in family_scores:
                family_scores["Metabolic"] += strength

        if "infection" in event or "immune" in event:
            if "Immune" in family_scores:
                family_scores["Immune"] += strength

    return family_scores
