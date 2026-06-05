# Problem 4: Appointment No-Show Rate
# Prompt: You receive a stream of (clinician_id, showed_up: bool) for every appointment.
# Build a class that tracks each clinician’s no-show rate over their last 10 appointments, and can return a list of clinicians whose no-show rate exceeds a given threshold.

# Expected methods:

# ingest(clinician_id, showed_up)
# no_show_rate(clinician_id) → float
# flagged_clinicians(threshold=0.3) → list of clinician_ids
# Think about: What is the Big O of flagged_clinicians? Can you optimize it?


stream = [
    # dr_smith: mostly no-shows → should be flagged
    ("dr_smith", True),
    ("dr_smith", False),
    ("dr_smith", False),
    ("dr_smith", False),
    ("dr_smith", True),
    ("dr_smith", False),
    ("dr_smith", False),
    ("dr_smith", False),
    ("dr_smith", True),
    ("dr_smith", False),
    # window full (10): 3 True, 7 False → no-show rate = 0.7
    # dr_jones: reliable, rarely misses → should NOT be flagged
    ("dr_jones", True),
    ("dr_jones", True),
    ("dr_jones", True),
    ("dr_jones", True),
    ("dr_jones", False),
    ("dr_jones", True),
    ("dr_jones", True),
    ("dr_jones", True),
    ("dr_jones", True),
    ("dr_jones", True),
    # window full (10): 9 True, 1 False → no-show rate = 0.1
    # dr_patel: exactly at boundary → 0.3 should NOT be flagged (needs to exceed)
    ("dr_patel", True),
    ("dr_patel", True),
    ("dr_patel", True),
    ("dr_patel", True),
    ("dr_patel", True),
    ("dr_patel", True),
    ("dr_patel", True),
    ("dr_patel", False),
    ("dr_patel", False),
    ("dr_patel", False),
    # window full (10): 7 True, 3 False → no-show rate = 0.3 (exactly at threshold)
    # dr_lee: window overflow — oldest events should be evicted
    ("dr_lee", False),
    ("dr_lee", False),
    ("dr_lee", False),
    ("dr_lee", False),
    ("dr_lee", False),  # first 5: all no-shows
    ("dr_lee", True),
    ("dr_lee", True),
    ("dr_lee", True),
    ("dr_lee", True),
    ("dr_lee", True),  # next 5: all showed up → window full, rate = 0.5
    ("dr_lee", True),
    ("dr_lee", True),
    ("dr_lee", True),
    ("dr_lee", True),
    ("dr_lee", True),  # 5 more: evicts the 5 no-shows → rate should drop to 0.0
    # dr_chen: only 2 events (under-filled window)
    ("dr_chen", False),
    ("dr_chen", False),
    # window has 2: 0 True, 2 False → no-show rate = 1.0, should be flagged
]

from collections import defaultdict, deque


class SolutionName:
    def __init__(self, k):
        self.k = k
        self.data = defaultdict(lambda: deque(maxlen=k))
        self._avgs = defaultdict(float)

    def _avg(self, clinician_id):
        m = list(self.data[clinician_id])
        return 1 - (sum(m) / len(m))

    def ingest(self, clinician_id, score):
        self.data[clinician_id].append(score)
        m = list(self.data[clinician_id])
        if len(m) < self.k:
            return

        self._avgs[clinician_id] = self._avg(clinician_id)

    def no_show_rate(self, clinician_id):
        return self._avgs[clinician_id]

    def flagged_clinicians(self, threshold=0.3):
        return [c for c, v in self._avgs.items() if v < threshold]


# Test it
tracker = SolutionName(k=10)
for key, value in stream:
    tracker.ingest(key, value)
    print(f"{key}: no_show_rate={tracker.no_show_rate(key):.2f}  # window: {list(tracker.data[key])}")

print("\n--- Final rates ---")
for cid in tracker._avgs:
    print(f"  {cid}: {tracker.no_show_rate(cid):.2f}")

print(f"\nFlagged (threshold=0.3): {tracker.flagged_clinicians(0.30)}")
# Expected: dr_smith (0.7), dr_chen (1.0)
# NOT flagged: dr_jones (0.1), dr_patel (0.3 — not exceeding), dr_lee (0.0 — evicted no-shows)
