# Problem 1: Session Note Deidentification
# Prompt: Given a therapy session note (string) and a set of known patient names,
# replace all occurrences of those names with [REDACTED]. Names may appear in different cases.

names = {"John Smith", "Jane Doe"}
note = "John Smith reported feeling better. His wife jane doe also attended."

# Expected: "[REDACTED] reported feeling better. His wife [REDACTED] also attended."

# Expected signature:
# def deidentify(note: str, names: set) -> str:

# Follow-ups:
# What if you also need to catch partial names like just “John”?
# How would you handle this at scale across millions of notes?
# What about names embedded in other words? (“Johnson” shouldn’t match “John”)

import re


def deidentify(note: str, names: set) -> str:

    sorted_names = sorted(names, key=len, reverse=True)
    sorted_names = [n.lower() for n in list(sorted_names)]

    for name in sorted_names:
        # \b = word boundary, prevents "John" matching inside "Johnson"
        pattern = re.compile(re.escape(name), re.IGNORECASE)
        note = pattern.sub("[REDACTED]", note)
    return note


print(deidentify(note, names))
