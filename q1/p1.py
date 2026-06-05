# Problem 1: Medication Adherence Tracker
# Prompt: You receive a stream of medication check-in events (patient_id, took_medication: bool).
# Build a class that tracks the adherence rate (% of True) over the last 5 check-ins per patient.

stream = [
    ("patient_1", True),
    ("patient_1", True),
    ("patient_1", False),
    ("patient_2", True),
    ("patient_1", True),
    ("patient_1", True),
    ("patient_1", False),  # window: [True, False, True, True, False] → 60%
]

from collections import defaultdict, deque


class SolutionName:
    def __init__(self, k=5):
        self.k = k
        self.data = defaultdict(lambda: deque(maxlen=k))

    def ingest(self, patient, took_meds):
        self.data[patient].append(took_meds)

    def query(self, patient):
        m = self.data[patient]
        if len(m) < 5 or m is None:
            return None

        return sum(m) / len(m)


# Test it
tracker = SolutionName(k=5)
for key, value in stream:
    tracker.ingest(key, value)
    print(f"{key}: {tracker.query(key)} || {tracker.data[key]}")
