# Problem 7: Therapy Note Keyword Extractor
# Prompt: Given a session note and a set of clinical concern keywords,
# return which keywords appear in the note along with their frequency. Case-insensitive matching.

keywords = {"anxiety", "depression", "sleep", "panic", "suicidal", "trauma"}

note = """Patient reports increased anxiety this week. Sleep has been poor,
waking up 3-4 times per night. No panic attacks. Discussed anxiety
management techniques and sleep hygiene."""

# extract(note, keywords)
# # → {"anxiety": 2, "sleep": 2, "panic": 1}
# # depression, suicidal, trauma not found → excluded from result

# Expected signature:

# def extract(note: str, keywords: set) -> dict:

# Follow-ups:

# Handle plural forms (“anxieties” → “anxiety”)
# What about multi-word keywords like “panic attack”?
# How would this work as a preprocessing step for an ML classifier?

import re
from collections import defaultdict


def extract(note: str, keywords: set) -> dict:
    note_lower = note.lower()
    results = defaultdict(int)
    for kw in keywords:
        count = len(re.findall(re.escape(kw), note_lower))
        if count > 0:
            results[kw] = count
    return dict(results)


print(extract(note, keywords))
