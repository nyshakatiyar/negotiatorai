def calculate_overall_score(scores):
    """
    Calculate weighted negotiation score.
    """

    weights = {
        "confidence": 0.20,
        "persuasiveness": 0.25,
        "evidence": 0.20,
        "communication": 0.15,
        "professionalism": 0.10,
        "strategy": 0.10
    }

    total = 0

    for metric, weight in weights.items():
        total += scores.get(metric, 0) * weight

    return round(total)


def calculate_difficulty(overall_score, current_difficulty):
    """
    Adapt HR difficulty based on candidate performance.
    """

    if overall_score >= 90:
        current_difficulty += 1

    elif overall_score >= 75:
        current_difficulty = current_difficulty

    elif overall_score < 60:
        current_difficulty -= 1

    return max(1, min(5, current_difficulty))


def difficulty_description(level):
    descriptions = {
        1: "Friendly and supportive",
        2: "Professional",
        3: "Challenging",
        4: "Aggressive",
        5: "Executive-level pressure"
    }

    return descriptions.get(level, "Professional")