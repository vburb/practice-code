# Problem 3: Therapy Outcome Classifier (Rule-Based)
# Prompt: Given a patient’s history of PHQ-9 scores (depression screening, 0-27), classify their trajectory.
# Build a function that takes a list of scores and returns a classification.

# Scoring rules:

# Remission: latest score < 5 AND decreased by at least 50% from first score
# Responding: latest score decreased by at least 50% from first score but still >= 5
# Improving: latest score is lower than first score but < 50% decrease
# No change: latest score is within ±10% of first score
# Worsening: latest score is higher than first score


# classify([18, 15, 12, 8])     # "improving" (56% drop but latest >= 5... wait, 56% drop → "responding")
# classify([20, 18, 15, 3])     # "remission" (85% drop, latest < 5)
# classify([10, 11, 10, 9])     # "no change" (10% drop, within ±10%)
# classify([8, 10, 12, 15])     # "worsening"
# classify([22, 20, 15, 10])    # "responding" (55% drop, latest >= 5)

# Expected signature:

# def classify(scores: list[int]) -> str:

# Follow-ups:

# What if you need to handle missing/skipped assessments?
# How would you unit test edge cases?
# The clinician wants to override the classification — how do you design that?


def classify(scores: list[int]) -> str:
    if len(scores) < 2:
        return "insufficient data"

    first = scores[0]
    latest = scores[-1]

    # Percent change from first to latest
    if first == 0:
        pct_change = 0.0
    else:
        pct_change = (first - latest) / first  # positive = improvement

    # Apply rules in order of specificity
    if pct_change >= 0.5 and latest < 5:
        return "remission"
    elif pct_change >= 0.5:
        return "responding"
    elif abs(pct_change) <= 0.10:
        return "no change"
    elif latest < first and pct_change < 0.5:
        return "improving"
    elif latest > first:
        return "worsening"
    else:
        return "no change"  # fallback


print(classify([18, 15, 12, 8]))  #  , 56% drop → "responding")
print(classify([20, 18, 15, 3]))  # "remission" (85% drop, latest < 5)
print(classify([10, 11, 10, 9]))  # "no change" (10% drop, within ±10%)
print(classify([8, 10, 12, 15]))  # "worsening"
print(classify([22, 20, 15, 10]))  # "responding" (55% drop, latest >= 5)
