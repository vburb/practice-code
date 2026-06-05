# Prompt: You receive a stream of (patient_id, session_score).
# Build a class that determines if a patient is improving, declining, or stable based on their last 4 scores.

# Improving: each score >= the one before it (monotonically non-decreasing)
# Declining: each score <= the one before it (monotonically non-increasing)
# Stable: otherwise

stream = [
    ("patient_1", 60),
    ("patient_1", 65),
    ("patient_1", 70),
    ("patient_1", 80),  # → "improving"
    ("patient_1", 75),  # [65, 70, 80, 75] → "stable"
    ("patient_2", 90),
    ("patient_2", 85),
    ("patient_2", 80),
    ("patient_2", 70),  # → "declining"
]


from collections import defaultdict, deque


class SolutionName:
    def __init__(self, k):
        self.k = k
        self.data = defaultdict(lambda: deque(maxlen=k))

    def ingest(self, patient, score):
        self.data[patient].append(score)

    def query(self, patient):
        m = list(self.data[patient])
        if len(m) < self.k:
            return None

        improving = all(a < b for a, b in zip(m, m[1:]))
        declining = all(a > b for a, b in zip(m, m[1:]))

        if improving:
            return "improving"
        if declining:
            return "declining"
        return "stable"


# Test it
tracker = SolutionName(k=4)
for key, value in stream:
    tracker.ingest(key, value)
    print(f"{key}: {tracker.query(key)}     # window:  {list(tracker.data[key])}")
