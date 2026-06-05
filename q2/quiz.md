# Applied AI / MLE Practice Problems — EHR Domain

Problems inspired by what an Applied AI Engineer at a therapy/clinician EHR platform might encounter.

---

## Problem 1: Session Note Deidentification

**Prompt:** Given a therapy session note (string) and a set of known patient names, replace all occurrences of those names with `[REDACTED]`. Names may appear in different cases.

```python
names = {"John Smith", "Jane Doe"}
note = "John Smith reported feeling better. His wife jane doe also attended."

# Expected: "[REDACTED] reported feeling better. His wife [REDACTED] also attended."
```

**Expected signature:**
```python
def deidentify(note: str, names: set) -> str:
```

**Follow-ups:**
- What if you also need to catch partial names like just "John"?
- How would you handle this at scale across millions of notes?
- What about names embedded in other words? ("Johnson" shouldn't match "John")

---

## Problem 2: Appointment Conflict Detector

**Prompt:** A clinician has a list of existing appointments as `(start, end)` tuples in minutes from midnight. Given a proposed new appointment, determine if it conflicts with any existing one.

```python
existing = [(540, 600), (660, 720), (780, 840)]
# 9:00-10:00, 11:00-12:00, 1:00-2:00

is_conflict(existing, (570, 630))  # True — overlaps with first
is_conflict(existing, (600, 660))  # False — exactly between
is_conflict(existing, (700, 800))  # True — overlaps with second and third
```

**Expected signature:**
```python
def is_conflict(existing: list[tuple], proposed: tuple) -> bool:
```

**Follow-ups:**
- Return ALL conflicting appointments, not just True/False
- What's the Big O? Can you do better than O(n) with sorted intervals?
- Add buffer time (e.g., 15 min between sessions)

---

## Problem 3: Therapy Outcome Classifier (Rule-Based)

**Prompt:** Given a patient's history of PHQ-9 scores (depression screening, 0-27), classify their trajectory. Build a function that takes a list of scores and returns a classification.

Scoring rules:
- **Remission:** latest score < 5 AND decreased by at least 50% from first score
- **Responding:** latest score decreased by at least 50% from first score but still >= 5
- **Improving:** latest score is lower than first score but < 50% decrease
- **No change:** latest score is within ±10% of first score
- **Worsening:** latest score is higher than first score

```python
classify([18, 15, 12, 8])     # "improving" (56% drop but latest >= 5... wait, 
                                #  56% drop → "responding")
classify([20, 18, 15, 3])     # "remission" (85% drop, latest < 5)
classify([10, 11, 10, 9])     # "no change" (10% drop, within ±10%)
classify([8, 10, 12, 15])     # "worsening"
classify([22, 20, 15, 10])    # "responding" (55% drop, latest >= 5)
```

**Expected signature:**
```python
def classify(scores: list[int]) -> str:
```

**Follow-ups:**
- What if you need to handle missing/skipped assessments?
- How would you unit test edge cases?
- The clinician wants to override the classification — how do you design that?

---

## Problem 4: Insurance Eligibility Matcher

**Prompt:** Given a list of clinician profiles (each with a set of accepted insurance plans) and a patient's insurance plan, return all matching clinicians sorted by number of total accepted plans (fewer = more specialized, rank first).

```python
clinicians = [
    {"name": "Dr. Smith", "plans": {"Aetna", "BlueCross", "Cigna", "United"}},
    {"name": "Dr. Jones", "plans": {"Aetna", "Cigna"}},
    {"name": "Dr. Patel", "plans": {"BlueCross", "Kaiser"}},
    {"name": "Dr. Lee", "plans": {"Aetna", "Medicare"}},
]

match(clinicians, "Aetna")
# → [Dr. Jones (2 plans), Dr. Lee (2 plans), Dr. Smith (4 plans)]
# Dr. Patel excluded — doesn't accept Aetna
```

**Expected signature:**
```python
def match(clinicians: list[dict], patient_plan: str) -> list[str]:
```

**Follow-ups:**
- Add a secondary sort by name alphabetically
- What data structure would you use if you had 100k clinicians and needed sub-millisecond lookups?
- How would you handle plan name variations? ("Blue Cross" vs "BlueCross" vs "BCBS")

---

## Problem 5: Session Duration Anomaly Detection

**Prompt:** Given a dictionary of `{clinician_id: [session_durations]}`, flag sessions that are statistical outliers. A session is an outlier if it's more than 2 standard deviations from that clinician's mean.

```python
sessions = {
    "dr_smith": [45, 50, 47, 52, 48, 120, 46, 51],  # 120 is an outlier
    "dr_jones": [30, 28, 32, 29, 31, 30],            # no outliers
}

find_outliers(sessions)
# → {"dr_smith": [120]}
```

**Expected signature:**
```python
def find_outliers(sessions: dict) -> dict:
```

**Think about:** Can you implement mean and std dev from scratch without numpy?

```python
import math

def std_dev(values):
    mean = sum(values) / len(values)
    variance = sum((x - mean) ** 2 for x in values) / len(values)
    return math.sqrt(variance)
```

---

## Problem 6: Recurring Appointment Generator

**Prompt:** Given a start date, recurrence rule (weekly, biweekly, monthly), and a count, generate the list of appointment dates. Skip any dates that fall on weekends.

```python
from datetime import date

generate(start=date(2026, 4, 13), rule="weekly", count=5)
# → [date(4/13), date(4/20), date(4/27), date(5/4), date(5/11)]

generate(start=date(2026, 4, 17), rule="weekly", count=3)  # Friday start
# → [date(4/17), date(4/24), date(5/1)]
# If any land on Sat/Sun, skip and continue to next valid date
```

**Expected signature:**
```python
def generate(start: date, rule: str, count: int) -> list[date]:
```

**Follow-ups:**
- Handle holidays as skip dates too
- What if the clinician wants "first Monday of each month"?
- Return as ISO strings instead of date objects

---

## Problem 7: Therapy Note Keyword Extractor

**Prompt:** Given a session note and a set of clinical concern keywords, return which keywords appear in the note along with their frequency. Case-insensitive matching.

```python
keywords = {"anxiety", "depression", "sleep", "panic", "suicidal", "trauma"}

note = """Patient reports increased anxiety this week. Sleep has been poor, 
waking up 3-4 times per night. No panic attacks. Discussed anxiety 
management techniques and sleep hygiene."""

extract(note, keywords)
# → {"anxiety": 2, "sleep": 2, "panic": 1}
# depression, suicidal, trauma not found → excluded from result
```

**Expected signature:**
```python
def extract(note: str, keywords: set) -> dict:
```

**Follow-ups:**
- Handle plural forms ("anxieties" → "anxiety")
- What about multi-word keywords like "panic attack"?
- How would this work as a preprocessing step for an ML classifier?

---

## Problem 8: Patient Risk Scoring

**Prompt:** Build a simple risk scoring system. Given a patient record (dict), compute a risk score based on weighted factors.

```python
weights = {
    "missed_appointments": 10,    # points per missed appt
    "declining_scores": 25,       # flat points if True
    "no_emergency_contact": 15,   # flat points if True
    "days_since_last_session": 0.5  # points per day
}

patient = {
    "name": "Jane Doe",
    "missed_appointments": 3,
    "declining_scores": True,
    "no_emergency_contact": False,
    "days_since_last_session": 45
}

risk_score(patient, weights)
# → 10*3 + 25*1 + 15*0 + 0.5*45 = 30 + 25 + 0 + 22.5 = 77.5
```

**Expected signature:**
```python
def risk_score(patient: dict, weights: dict) -> float:
```

**Follow-ups:**
- Normalize the score to 0-100 range
- Rank a list of patients by risk
- How would you transition this from rules to ML?

---

## Problem 9: Caseload Balancer

**Prompt:** Given a dict of `{clinician_id: current_patient_count}` and a list of new patients to assign, distribute new patients to minimize the max caseload across clinicians.

```python
caseloads = {"dr_smith": 25, "dr_jones": 30, "dr_patel": 20}
new_patients = 7

balance(caseloads, new_patients)
# → {"dr_smith": 27, "dr_jones": 30, "dr_patel": 27}
# Fills lowest first to even things out
```

**Expected signature:**
```python
def balance(caseloads: dict, new_patients: int) -> dict:
```

**Hint:** Think about using a min-heap.

```python
import heapq
```

**Follow-ups:**
- Add a max capacity per clinician
- What if clinicians have specialty constraints?
- What's the Big O?

---

## Problem 10: Tokenizer for Clinical NLP

**Prompt:** Build a simple tokenizer for clinical notes that handles common abbreviations and keeps hyphenated terms together.

Rules:
- Split on whitespace and punctuation EXCEPT hyphens within words
- Keep abbreviations intact: "pt.", "dx.", "tx.", "hx."
- Lowercase everything
- Remove standalone punctuation tokens

```python
note = "Pt. reports moderate-to-severe anxiety. Dx. is GAD; tx. plan includes CBT."

tokenize(note)
# → ["pt.", "reports", "moderate-to-severe", "anxiety", "dx.", "is", 
#     "gad", "tx.", "plan", "includes", "cbt"]
```

**Expected signature:**
```python
def tokenize(note: str) -> list[str]:
```

**Follow-ups:**
- How would you extend this to handle negation? ("no anxiety" vs "anxiety")
- Build a vocabulary index from a corpus of notes
- How does this compare to what a real NLP tokenizer (spaCy, BERT) does?

---

## Difficulty Ranking

| # | Problem | Core Concept | Difficulty |
|---|---------|-------------|------------|
| 1 | Deidentification | String manipulation, regex | ⭐ Easy |
| 2 | Conflict Detection | Interval overlap logic | ⭐ Easy |
| 3 | Outcome Classifier | Conditional logic, edge cases | ⭐⭐ Medium |
| 4 | Insurance Matcher | Filtering, sorting, set membership | ⭐⭐ Medium |
| 5 | Anomaly Detection | Statistics from scratch | ⭐⭐ Medium |
| 6 | Recurring Dates | datetime, business logic | ⭐⭐ Medium |
| 7 | Keyword Extractor | Text processing, counting | ⭐ Easy |
| 8 | Risk Scoring | Dict traversal, weighted sum | ⭐ Easy |
| 9 | Caseload Balancer | Heap / greedy algorithm | ⭐⭐⭐ Hard |
| 10 | Clinical Tokenizer | Regex, NLP preprocessing | ⭐⭐⭐ Hard |
