def normalize_safety_signals(adrs: list[dict]) -> dict:
    """
    Normalize raw ADR safety signals into an interpretable risk summary.
    """

    if not adrs:
        return {
            "max_signal": 0,
            "mean_signal": 0,
            "high_risk_events": [],
            "risk_level": "LOW",
        }

    signals = [adr["signal_strength"] for adr in adrs if adr.get("signal_strength")]

    max_signal = max(signals)
    mean_signal = sum(signals) / len(signals)

    HIGH_RISK_THRESHOLD = 500

    high_risk_events = [
        adr["event"]
        for adr in adrs
        if adr.get("signal_strength", 0) >= HIGH_RISK_THRESHOLD
    ]

    if max_signal >= 1000:
        risk_level = "HIGH"
    elif max_signal >= 100:
        risk_level = "MEDIUM"
    else:
        risk_level = "LOW"

    return {
        "max_signal": round(max_signal, 2),
        "mean_signal": round(mean_signal, 2),
        "high_risk_events": high_risk_events,
        "risk_level": risk_level,
    }
