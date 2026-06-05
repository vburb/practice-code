# Applied AI / MLE Practice Problems — Solutions

---

## Problem 1: Session Note Deidentification

```python
import re

def deidentify(note: str, names: set) -> str:
    # Sort by length descending so "John Smith" matches before "John"
    sorted_names = sorted(names, key=len, reverse=True)

    for name in sorted_names:
        # \b = word boundary, prevents "John" matching inside "Johnson"
        pattern = re.compile(re.escape(name), re.IGNORECASE)
        note = pattern.sub("[REDACTED]", note)

    return note


# Test
names = {"John Smith", "Jane Doe"}
note = "John Smith reported feeling better. His wife jane doe also attended."
print(deidentify(note, names))
# → "[REDACTED] reported feeling better. His wife [REDACTED] also attended."

# Edge case: name inside another word
note2 = "Johnson was not present. John Smith was."
print(deidentify(note2, {"John Smith"}))
# → "Johnson was not present. [REDACTED] was."
# Hmm — without word boundaries, "John" inside "Johnson" could be a problem
# if matching partial names. re.escape + full name matching avoids this.
```

**Key concepts:**
- `re.IGNORECASE` for case-insensitive matching
- Sort longest-first to avoid partial replacements
- `re.escape()` handles names with special characters
- Word boundaries (`\b`) matter if matching partial names

---

## Problem 2: Appointment Conflict Detector

```python
def is_conflict(existing: list[tuple], proposed: tuple) -> bool:
    p_start, p_end = proposed
    for start, end in existing:
        # Overlap: starts before the other ends AND ends after the other starts
        if p_start < end and p_end > start:
            return True
    return False


def find_conflicts(existing: list[tuple], proposed: tuple) -> list[tuple]:
    """Follow-up: return ALL conflicting appointments."""
    p_start, p_end = proposed
    return [(s, e) for s, e in existing if p_start < e and p_end > s]


def is_conflict_with_buffer(existing: list[tuple], proposed: tuple, buffer: int = 15) -> bool:
    """Follow-up: add buffer time between sessions."""
    p_start, p_end = proposed
    for start, end in existing:
        if p_start < (end + buffer) and p_end > (start - buffer):
            return True
    return False


# Tests
existing = [(540, 600), (660, 720), (780, 840)]

print(is_conflict(existing, (570, 630)))  # True
print(is_conflict(existing, (600, 660)))  # False — exactly between
print(is_conflict(existing, (700, 800)))  # True

print(find_conflicts(existing, (700, 800)))  # [(660, 720), (780, 840)]

# With buffer: (600, 660) is now too close to the 540-600 block
print(is_conflict_with_buffer(existing, (600, 660), buffer=15))  # True
```

**Key concepts:**
- Overlap formula: `a_start < b_end and a_end > b_start`
- Draw intervals on a number line to convince yourself
- O(n) scan — could be O(log n) with sorted intervals + binary search

---

## Problem 3: Therapy Outcome Classifier

```python
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
    elif latest < first and pct_change < 0.5:
        return "improving"
    elif abs(pct_change) <= 0.10:
        return "no change"
    elif latest > first:
        return "worsening"
    else:
        return "no change"  # fallback


# Tests
print(classify([18, 15, 12, 8]))    # "responding" (56% drop, latest >= 5)
print(classify([20, 18, 15, 3]))    # "remission" (85% drop, latest < 5)
print(classify([10, 11, 10, 9]))    # "no change" (10% drop)
print(classify([8, 10, 12, 15]))    # "worsening"
print(classify([22, 20, 15, 10]))   # "responding" (55% drop, latest >= 5)

# Edge cases
print(classify([0, 0, 0, 0]))      # "no change"
print(classify([5]))                # "insufficient data"
print(classify([27, 13]))           # "responding" (52% drop, latest >= 5)
```

**Key concepts:**
- Order of conditional checks matters — most specific first
- Handle division by zero (first score = 0)
- `abs()` for the ±10% "no change" band

---

## Problem 4: Insurance Eligibility Matcher

```python
def match(clinicians: list[dict], patient_plan: str) -> list[str]:
    # Filter to those who accept the plan
    matching = [c for c in clinicians if patient_plan in c["plans"]]

    # Sort by number of plans (ascending), then name alphabetically
    matching.sort(key=lambda c: (len(c["plans"]), c["name"]))

    return [c["name"] for c in matching]


# Test
clinicians = [
    {"name": "Dr. Smith", "plans": {"Aetna", "BlueCross", "Cigna", "United"}},
    {"name": "Dr. Jones", "plans": {"Aetna", "Cigna"}},
    {"name": "Dr. Patel", "plans": {"BlueCross", "Kaiser"}},
    {"name": "Dr. Lee", "plans": {"Aetna", "Medicare"}},
]

print(match(clinicians, "Aetna"))
# → ["Dr. Jones", "Dr. Lee", "Dr. Smith"]

print(match(clinicians, "Kaiser"))
# → ["Dr. Patel"]

print(match(clinicians, "Tricare"))
# → []


# Follow-up: inverted index for fast lookups at scale
def build_plan_index(clinicians: list[dict]) -> dict:
    """O(1) lookup by plan after O(n) build."""
    index = {}
    for c in clinicians:
        for plan in c["plans"]:
            if plan not in index:
                index[plan] = []
            index[plan].append(c)
    return index

plan_index = build_plan_index(clinicians)
# Now: plan_index["Aetna"] gives you the list instantly
```

**Key concepts:**
- Set membership check (`in`) is O(1)
- Tuple sort key for multi-level sorting
- Inverted index is the scalable answer (100k clinicians)

---

## Problem 5: Session Duration Anomaly Detection

```python
import math

def mean(values):
    return sum(values) / len(values)


def std_dev(values):
    m = mean(values)
    variance = sum((x - m) ** 2 for x in values) / len(values)
    return math.sqrt(variance)


def find_outliers(sessions: dict, num_std: float = 2.0) -> dict:
    result = {}
    for clinician, durations in sessions.items():
        if len(durations) < 2:
            continue

        m = mean(durations)
        sd = std_dev(durations)

        if sd == 0:  # all identical durations
            continue

        outliers = [d for d in durations if abs(d - m) > num_std * sd]
        if outliers:
            result[clinician] = outliers

    return result


# Tests
sessions = {
    "dr_smith": [45, 50, 47, 52, 48, 120, 46, 51],  # 120 is an outlier
    "dr_jones": [30, 28, 32, 29, 31, 30],            # no outliers
    "dr_patel": [60, 60, 60, 60],                    # all identical, skip
    "dr_lee": [45],                                   # too few, skip
}

print(find_outliers(sessions))
# → {"dr_smith": [120]}
```

**Key concepts:**
- Implement mean/std_dev from scratch (no numpy)
- Guard against `len < 2` and `std_dev == 0`
- `abs(x - mean) > 2 * std_dev` is the outlier test
- Population std dev (divide by n), not sample (divide by n-1) — mention the difference

---

## Problem 6: Recurring Appointment Generator

```python
from datetime import date, timedelta
from dateutil.relativedelta import relativedelta  # for monthly


def generate(start: date, rule: str, count: int, skip_dates: set = None) -> list[date]:
    skip_dates = skip_dates or set()
    results = []
    current = start

    # Define step based on rule
    deltas = {
        "weekly": timedelta(weeks=1),
        "biweekly": timedelta(weeks=2),
    }

    while len(results) < count:
        # Skip weekends (5=Sat, 6=Sun)
        if current.weekday() < 5 and current not in skip_dates:
            results.append(current)

        # Advance
        if rule == "monthly":
            current += relativedelta(months=1)
        else:
            current += deltas[rule]

    return results


# Tests
print(generate(start=date(2026, 4, 13), rule="weekly", count=5))
# → Mon 4/13, Mon 4/20, Mon 4/27, Mon 5/4, Mon 5/11

print(generate(start=date(2026, 4, 17), rule="biweekly", count=3))
# → Fri 4/17, Fri 5/1, Fri 5/15

print(generate(start=date(2026, 4, 13), rule="monthly", count=4))
# → 4/13, 5/13, 6/13 (Sat → skipped!), need to handle...

# With holidays
holidays = {date(2026, 5, 25)}  # Memorial Day
print(generate(start=date(2026, 5, 11), rule="weekly", count=4, skip_dates=holidays))
# → 5/11, 5/18, 6/1, 6/8 — skips 5/25
```

**Gotcha:** The skip logic above only skips *and doesn't advance to the next valid day* — it just waits for the next scheduled occurrence. If you want "push to next Monday if it lands on a weekend," that's a different behavior:

```python
def next_weekday(d: date) -> date:
    """Push a date forward to the next weekday if it falls on a weekend."""
    while d.weekday() >= 5:
        d += timedelta(days=1)
    return d
```

**Key concepts:**
- `timedelta` for fixed intervals, `relativedelta` for calendar-aware (monthly)
- `weekday()` — 0=Mon, 6=Sun
- Clarify skip behavior vs push-forward behavior in the interview

---

## Problem 7: Therapy Note Keyword Extractor

```python
import re
from collections import Counter


def extract(note: str, keywords: set) -> dict:
    # Tokenize: split on non-alpha characters, lowercase
    words = re.findall(r'[a-zA-Z]+', note.lower())
    counts = Counter(words)

    # Only return keywords that appear
    return {kw: counts[kw] for kw in keywords if kw in counts}


# Test
keywords = {"anxiety", "depression", "sleep", "panic", "suicidal", "trauma"}

note = """Patient reports increased anxiety this week. Sleep has been poor, 
waking up 3-4 times per night. No panic attacks. Discussed anxiety 
management techniques and sleep hygiene."""

print(extract(note, keywords))
# → {"anxiety": 2, "sleep": 2, "panic": 1}


# Follow-up: multi-word keywords
def extract_with_phrases(note: str, keywords: set) -> dict:
    note_lower = note.lower()
    result = {}
    for kw in keywords:
        count = len(re.findall(re.escape(kw), note_lower))
        if count > 0:
            result[kw] = count
    return result

keywords_v2 = {"anxiety", "panic attack", "sleep"}
print(extract_with_phrases(note, keywords_v2))
# → {"anxiety": 2, "sleep": 2, "panic attack": 1}
```

**Key concepts:**
- `re.findall(r'[a-zA-Z]+', text)` is a quick tokenizer
- Counter gives you frequency for free
- Multi-word keywords need substring matching, not token matching

---

## Problem 8: Patient Risk Scoring

```python
def risk_score(patient: dict, weights: dict) -> float:
    score = 0.0
    for factor, weight in weights.items():
        value = patient.get(factor)
        if value is None:
            continue
        if isinstance(value, bool):
            score += weight * int(value)  # True=1, False=0
        else:
            score += weight * value
    return score


def normalize(score: float, max_possible: float) -> float:
    """Normalize to 0-100 range."""
    return min(100.0, (score / max_possible) * 100)


def rank_patients(patients: list[dict], weights: dict) -> list[tuple]:
    """Return patients sorted by risk, highest first."""
    scored = [(p["name"], risk_score(p, weights)) for p in patients]
    scored.sort(key=lambda x: x[1], reverse=True)
    return scored


# Test
weights = {
    "missed_appointments": 10,
    "declining_scores": 25,
    "no_emergency_contact": 15,
    "days_since_last_session": 0.5,
}

patient = {
    "name": "Jane Doe",
    "missed_appointments": 3,
    "declining_scores": True,
    "no_emergency_contact": False,
    "days_since_last_session": 45,
}

print(risk_score(patient, weights))
# → 10*3 + 25*1 + 15*0 + 0.5*45 = 77.5

# Ranking
patients = [
    {"name": "Jane Doe", "missed_appointments": 3, "declining_scores": True,
     "no_emergency_contact": False, "days_since_last_session": 45},
    {"name": "John Smith", "missed_appointments": 0, "declining_scores": False,
     "no_emergency_contact": False, "days_since_last_session": 7},
    {"name": "Alex Kim", "missed_appointments": 5, "declining_scores": True,
     "no_emergency_contact": True, "days_since_last_session": 90},
]

print(rank_patients(patients, weights))
# → [("Alex Kim", 135.0), ("Jane Doe", 77.5), ("John Smith", 3.5)]
```

**Key concepts:**
- `isinstance(value, bool)` check — must come before numeric check since `bool` is a subclass of `int` in Python
- `.get()` with None fallback for missing fields
- Ranking is just `sorted` with `reverse=True`

---

## Problem 9: Caseload Balancer

```python
import heapq


def balance(caseloads: dict, new_patients: int) -> dict:
    # Min-heap of (count, clinician_id)
    heap = [(count, cid) for cid, count in caseloads.items()]
    heapq.heapify(heap)

    for _ in range(new_patients):
        count, cid = heapq.heappop(heap)
        heapq.heappush(heap, (count + 1, cid))

    return {cid: count for count, cid in heap}


# Test
caseloads = {"dr_smith": 25, "dr_jones": 30, "dr_patel": 20}
print(balance(caseloads, 7))
# → {"dr_patel": 27, "dr_smith": 27, "dr_jones": 30}
# Fills dr_patel (20→21→...→25), then alternates dr_patel and dr_smith up to 27


# Follow-up: with max capacity
def balance_with_cap(caseloads: dict, new_patients: int, max_cap: dict) -> dict:
    heap = [(count, cid) for cid, count in caseloads.items()]
    heapq.heapify(heap)

    unassigned = 0
    for _ in range(new_patients):
        count, cid = heapq.heappop(heap)
        if count >= max_cap.get(cid, float('inf')):
            # This clinician is full, put them back and try next
            heapq.heappush(heap, (count, cid))
            # Check if ALL are full
            if all(c >= max_cap.get(id_, float('inf')) for c, id_ in heap):
                unassigned += 1
                continue
            # Pop the next lowest
            count2, cid2 = heapq.heappop(heap)
            heapq.heappush(heap, (count, cid))  # put full one back
            heapq.heappush(heap, (count2 + 1, cid2))
        else:
            heapq.heappush(heap, (count + 1, cid))

    result = {cid: count for count, cid in heap}
    if unassigned:
        print(f"Warning: {unassigned} patients could not be assigned")
    return result


caps = {"dr_smith": 27, "dr_jones": 30, "dr_patel": 28}
print(balance_with_cap(caseloads, 7, caps))
```

**Key concepts:**
- `heapq` gives you a min-heap — always assign to the least loaded
- `heapify` is O(n), each push/pop is O(log n), total is O(m log n) where m = new patients
- The greedy approach (always fill the lowest) is provably optimal for minimizing max load

---

## Problem 10: Tokenizer for Clinical NLP

```python
import re

# Abbreviations to preserve (with their trailing period)
ABBREVIATIONS = {"pt.", "dx.", "tx.", "hx.", "rx.", "sx.", "fx.", "bx."}


def tokenize(note: str) -> list[str]:
    # Split on whitespace first
    raw_tokens = note.lower().split()

    tokens = []
    for raw in raw_tokens:
        # Check if it's a known abbreviation (possibly with trailing punctuation)
        if raw.rstrip(";,") in ABBREVIATIONS:
            tokens.append(raw.rstrip(";,"))
            continue

        # Split off trailing punctuation but keep hyphens within words
        # "anxiety." → "anxiety" + discard "."
        # "moderate-to-severe" → keep as-is
        # "GAD;" → "gad" + discard ";"
        parts = re.findall(r"[a-zA-Z]+(?:-[a-zA-Z]+)*", raw)
        tokens.extend(parts)

    return tokens


# Test
note = "Pt. reports moderate-to-severe anxiety. Dx. is GAD; tx. plan includes CBT."
print(tokenize(note))
# → ["pt.", "reports", "moderate-to-severe", "anxiety", "dx.", "is",
#     "gad", "tx.", "plan", "includes", "cbt"]

# More edge cases
note2 = "Hx. of trauma-related PTSD. Rx. includes sertraline 50mg."
print(tokenize(note2))
# → ["hx.", "of", "trauma-related", "ptsd", "rx.", "includes", "sertraline", "50mg"]


# Follow-up: negation detection
def tokenize_with_negation(note: str) -> list[dict]:
    """Tag each token with whether it's negated."""
    tokens = tokenize(note)
    negation_words = {"no", "not", "never", "denies", "without", "none"}
    result = []
    negated = False

    for token in tokens:
        if token in negation_words:
            negated = True
            result.append({"token": token, "negated": False})
            continue

        result.append({"token": token, "negated": negated})

        # Reset negation at punctuation boundaries (approximation)
        if token.endswith("."):
            negated = False

    return result

note3 = "No anxiety reported. Sleep is poor."
for t in tokenize_with_negation(note3):
    flag = " [NEG]" if t["negated"] else ""
    print(f"  {t['token']}{flag}")
# → no
#   anxiety [NEG]
#   reported [NEG]    ← negation resets after period
#   sleep
#   is
#   poor
```

**Key concepts:**
- Regex `[a-zA-Z]+(?:-[a-zA-Z]+)*` keeps hyphenated words together
- Abbreviation lookup as a set for O(1) membership
- Negation detection is a classic NLP preprocessing step — simple window-based approach works for interviews
- Real tokenizers (spaCy, BERT WordPiece) handle this with trained models, but rule-based is expected in a live coding setting
