# Problem 2: Peak Anxiety Score
# Prompt: You receive a stream of (patient_id, anxiety_score) from daily check-ins.
# Build a class that tracks the maximum anxiety score within a sliding window of the last 7 entries per patient.

stream = [
    ("patient_1", 3),
    ("patient_1", 7),
    ("patient_1", 5),
    ("patient_1", 2),
    ("patient_1", 8),
    ("patient_1", 4),
    ("patient_1", 6),
    ("patient_1", 1),  # window: [7,5,2,8,4,6,1] → max = 8
    ("patient_1", 3),  # window: [5,2,8,4,6,1,3] → max = 8
    ("patient_1", 2),  # window: [2,8,4,6,1,3,2] → max = 8
    ("patient_1", 1),  # window: [8,4,6,1,3,2,1] → max = 8
    ("patient_1", 1),  # window: [4,6,1,3,2,1,1] → max = 6  ← 8 evicted
]

from collections import defaultdict, deque


class SolutionName:
    def __init__(self, k):
        self.k = k
        self.data = defaultdict(lambda: deque(maxlen=k))

    def ingest(self, patient, score):
        self.data[patient].append(score)

    def query(self, patient):
        m = self.data[patient]
        if len(m) < self.k:
            return None
        return max(m)


# Test it
tracker = SolutionName(k=7)
for key, value in stream:
    tracker.ingest(key, value)
    print(f"{key}: {tracker.query(key)}     # window:  {list(tracker.data[key])}")
