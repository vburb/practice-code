# Problem 2: Appointment Conflict Detector
# Prompt: A clinician has a list of existing appointments as (start, end) tuples in minutes from midnight.
# Given a proposed new appointment, determine if it conflicts with any existing one.

existing = [(540, 600), (660, 720), (780, 840)]
# 9:00-10:00, 11:00-12:00, 1:00-2:00

# is_conflict(existing, (570, 630))  # True — overlaps with first
# is_conflict(existing, (600, 660))  # False — exactly between
# is_conflict(existing, (700, 800))  # True — overlaps with second and third

# Expected signature:

# def is_conflict(existing: list[tuple], proposed: tuple) -> bool:

# Follow-ups:

# Return ALL conflicting appointments, not just True/False
# What’s the Big O? Can you do better than O(n) with sorted intervals?
# Add buffer time (e.g., 15 min between sessions)


def is_conflict(existing: list[tuple], proposed: tuple) -> bool:

    p_start, p_end = proposed

    for start, end in existing:
        if p_start < end and p_end > start:
            return True
    return False


print(is_conflict(existing, (570, 630)))  # True — overlaps with first
print(is_conflict(existing, (600, 660)))  # False — exactly between
print(is_conflict(existing, (700, 800)))  # True — overlaps with second and third
