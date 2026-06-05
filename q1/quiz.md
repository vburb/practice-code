# Streaming Data Practice Problems

All problems follow the same pattern: ingest streaming events, maintain state per key, answer queries efficiently.

---

## Problem 1: Medication Adherence Tracker

**Prompt:** You receive a stream of medication check-in events `(patient_id, took_medication: bool)`. Build a class that tracks the adherence rate (% of True) over the last 5 check-ins per patient.

```python
stream = [
    ("patient_1", True),
    ("patient_1", True),
    ("patient_1", False),
    ("patient_2", True),
    ("patient_1", True),
    ("patient_1", True),
    ("patient_1", False),  # window: [True, False, True, True, False] → 60%
]
```

**Expected methods:**
- `ingest(patient_id, took_med)`
- `adherence_rate(patient_id)` → float between 0.0 and 1.0

---

## Problem 2: Peak Anxiety Score

**Prompt:** You receive a stream of `(patient_id, anxiety_score)` from daily check-ins. Build a class that tracks the **maximum** anxiety score within a sliding window of the last 7 entries per patient.

```python
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
```

**Expected methods:**
- `ingest(patient_id, score)`
- `peak_score(patient_id)` → int

**Bonus:** Can you do better than scanning the full window every time?

---

## Problem 3: Session Trend Detector

**Prompt:** You receive a stream of `(patient_id, session_score)`. Build a class that determines if a patient is **improving**, **declining**, or **stable** based on their last 4 scores.

- **Improving:** each score >= the one before it (monotonically non-decreasing)
- **Declining:** each score <= the one before it (monotonically non-increasing)
- **Stable:** otherwise

```python
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
```

**Expected methods:**
- `ingest(patient_id, score)`
- `trend(patient_id)` → `"improving"` | `"declining"` | `"stable"` | `None` (if < 2 scores)

---

## Problem 4: Appointment No-Show Rate

**Prompt:** You receive a stream of `(clinician_id, showed_up: bool)` for every appointment. Build a class that tracks each clinician's no-show rate over their last 10 appointments, and can return a list of clinicians whose no-show rate exceeds a given threshold.

```python
stream = [
    ("dr_smith", True),
    ("dr_smith", False),
    ("dr_smith", False),
    ("dr_jones", True),
    ("dr_jones", True),
    # ... more events
]
```

**Expected methods:**
- `ingest(clinician_id, showed_up)`
- `no_show_rate(clinician_id)` → float
- `flagged_clinicians(threshold=0.3)` → list of clinician_ids

**Think about:** What is the Big O of `flagged_clinicians`? Can you optimize it?

---

## Problem 5: Billing Code Frequency

**Prompt:** You receive a stream of `(clinician_id, billing_code)`. Build a class that tracks the **most frequently used billing code** per clinician across their last 20 billed sessions.

```python
stream = [
    ("dr_smith", "90834"),  # Individual therapy 45 min
    ("dr_smith", "90837"),  # Individual therapy 60 min
    ("dr_smith", "90834"),
    ("dr_smith", "90847"),  # Family therapy
    ("dr_smith", "90834"),
    # → most frequent for dr_smith: "90834"
]
```

**Expected methods:**
- `ingest(clinician_id, code)`
- `most_common(clinician_id)` → str (the billing code)

**Hint:** Think about what data structure pairs well with deque here.

---

## Starter Template

Use this for each problem:

```python
from collections import defaultdict, deque

class SolutionName:
    def __init__(self, k=3):
        self.k = k
        self.data = defaultdict(lambda: deque(maxlen=k))

    def ingest(self, key, value):
        # your code here
        pass

    def query(self, key):
        # your code here
        pass


# Test it
stream = [...]
tracker = SolutionName(k=...)
for key, value in stream:
    tracker.ingest(key, value)
    print(f"{key}: {tracker.query(key)}")
```

---

## Difficulty Ranking

| # | Problem | Core Concept | Difficulty |
|---|---------|-------------|------------|
| 1 | Medication Adherence | Boolean rate in sliding window | ⭐ Easy |
| 2 | Peak Anxiety Score | Max in sliding window | ⭐⭐ Medium |
| 3 | Session Trend | Pattern detection in window | ⭐⭐ Medium |
| 4 | No-Show Rate | Aggregation across all keys | ⭐⭐ Medium |
| 5 | Billing Code Frequency | Secondary data structure (Counter) | ⭐⭐⭐ Hard |
