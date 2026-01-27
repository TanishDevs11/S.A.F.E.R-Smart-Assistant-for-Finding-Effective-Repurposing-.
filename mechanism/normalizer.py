def normalize_direction_of_effect(targets: list[dict]) -> list[dict]:
    """
    Normalize action types into biological direction of effect.

    Args:
        targets (list[dict]): Canonical targets from Stage 2.2

    Returns:
        list[dict]: Targets with normalized direction_of_effect
    """

    loss_of_function = {"INHIBITOR", "ANTAGONIST", "BLOCKER"}
    gain_of_function = {"AGONIST", "ACTIVATOR"}

    normalized = []

    for target in targets:
        action_type = target.get("action_type", "").upper()

        if action_type in loss_of_function:
            direction = "loss_of_function"
        elif action_type in gain_of_function:
            direction = "gain_of_function"
        else:
            direction = "unknown"

        normalized.append(
            {
                **target,
                "direction_of_effect": direction,
            }
        )

    if not normalized:
        raise ValueError("No targets available for direction normalization")

    return normalized
