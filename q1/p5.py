# Problem 5: Billing Code Frequency
# Prompt: You receive a stream of (clinician_id, billing_code).
#  Build a class that tracks the most frequently used billing code per clinician across their last 20 billed sessions.

stream = [
    ("dr_smith", "90834"),  # Individual therapy 45 min
    ("dr_smith", "90837"),  # Individual therapy 60 min
    ("dr_smith", "90834"),
    ("dr_smith", "90847"),  # Family therapy
    ("dr_smith", "90834"),
    # → most frequent for dr_smith: "90834"
]

# Expected methods:

# ingest(clinician_id, code)
# most_common(clinician_id) → str (the billing code)
# Hint: Think about what data structure pairs well with deque here.


from collections import Counter, defaultdict, deque


class SolutionName:
    def __init__(self, k):
        self.k = k
        self.data = defaultdict(lambda: deque(maxlen=k))

    def ingest(self, clinician_id, billing_code):
        self.data[clinician_id].append(billing_code)

    def most_common(self, clinician_id):
        m = list(self.data[clinician_id])
        if not m:
            return None
        return Counter(m).most_common(1)[0][0]


# Test it
tracker = SolutionName(k=4)
for key, value in stream:
    tracker.ingest(key, value)
    print(f"{key}: {tracker.most_common(key)}     # window:  {list(tracker.data[key])}")
