# Problem 5: Session Duration Anomaly Detection
# Prompt: Given a dictionary of {clinician_id: [session_durations]},
# flag sessions that are statistical outliers. A session is an outlier if it’s more than 2
# standard deviations from that clinician’s mean.

sessions = {
    "dr_smith": [45, 50, 47, 52, 48, 120, 46, 51],  # 120 is an outlier
    "dr_jones": [30, 28, 32, 29, 31, 30],  # no outliers
    "dr_patel": [60, 60, 60, 60],  # all identical, skip
    "dr_lee": [45],  # too few, skip
}


# find_outliers(sessions)
# → {"dr_smith": [120]}

# Expected signature:

# def find_outliers(sessions: dict) -> dict:

# Think about: Can you implement mean and std dev from scratch without numpy?

import math


def mean(values):
    return sum(values) / len(values)


def std_dev(values):
    m = mean(values)
    variance = sum((x - m) ** 2 for x in values) / len(values)
    return math.sqrt(variance)


from collections import defaultdict


def find_outliers(sessions: dict) -> dict:
    outliers = defaultdict(list)

    for clinician, times in sessions.items():
        stddev = std_dev(times)
        m = mean(times)
        threshold_a = m + 2 * stddev
        threshold_b = m - 2 * stddev
        outlier_times = [t for t in times if t > threshold_a or t < threshold_b]
        if outlier_times:
            outliers[clinician] = outlier_times

    return dict(outliers)


print(find_outliers(sessions))
