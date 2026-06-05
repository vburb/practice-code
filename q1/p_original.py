## PROBLEM
# Ingest streaming data of patient therapy session scores and
# compute the averages of the 3 most recent scores by patient.

## INPUT
# Sample stream of events
stream = [
    ("patient_1", 85),
    ("patient_2", 70),
    ("patient_1", 90),
    ("patient_2", 65),
    ("patient_1", 75),
    ("patient_1", 95),  # should evict 85
    ("patient_2", 80),
]


## OUTPUT

from collections import defaultdict


class SessionTracker:
    def __init__(self, k=3):
        self.k = k
        self.scores = defaultdict(list)

    def ingest(self, patient_id, score):
        self.scores[patient_id].append(score)
        self.scores[patient_id] = self.scores[patient_id][-self.k :]

    def average(self, patient_id):
        s = self.scores[patient_id]

        if len(s) != 3 or s is None:
            return None

        return sum(s) / len(s)

    def get_values(self, patient_id):
        return self.scores[patient_id]


tracker = SessionTracker(k=3)

for patient_id, score in stream:
    tracker.ingest(patient_id, score)
    values = tracker.get_values(patient_id)
    avg = tracker.average(patient_id)
    print(f"{patient_id}: new score={score}, avg of last 3 = {avg}; values={values}")
