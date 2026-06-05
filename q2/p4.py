# Problem 4: Insurance Eligibility Matcher
# Prompt: Given a list of clinician profiles (each with a set of accepted insurance plans) and a patient’s insurance plan, return all matching clinicians sorted by number of total accepted plans (fewer = more specialized, rank first).

clinicians = [
    {"name": "Dr. Smith", "plans": {"Aetna", "BlueCross", "Cigna", "United"}},
    {"name": "Dr. Jones", "plans": {"Aetna", "Cigna"}},
    {"name": "Dr. Patel", "plans": {"BlueCross", "Kaiser"}},
    {"name": "Dr. Lee", "plans": {"Aetna", "Medicare"}},
]

# match(clinicians, "Aetna")
# # → [Dr. Jones (2 plans), Dr. Lee (2 plans), Dr. Smith (4 plans)]
# # Dr. Patel excluded — doesn't accept Aetna

# Expected signature:

# def match(clinicians: list[dict], patient_plan: str) -> list[str]:

# Follow-ups:

# Add a secondary sort by name alphabetically
# What data structure would you use if you had 100k clinicians and needed sub-millisecond lookups?
# How would you handle plan name variations? (“Blue Cross” vs “BlueCross” vs “BCBS”)


def match(clinicians: list[dict], patient_plan: str) -> list[str]:
    

