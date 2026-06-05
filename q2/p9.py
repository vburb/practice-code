# Problem 9: Caseload Balancer
# Prompt: Given a dict of {clinician_id: current_patient_count} and a list of new patients to assign, distribute new patients to minimize the max caseload across clinicians.

caseloads = {"dr_smith": 25, "dr_jones": 30, "dr_patel": 20}
new_patients = 7

# balance(caseloads, new_patients)
# # → {"dr_smith": 27, "dr_jones": 30, "dr_patel": 27}
# # Fills lowest first to even things out

# Expected signature:

# def balance(caseloads: dict, new_patients: int) -> dict:

# Hint: Think about using a min-heap.

# import heapq

# Follow-ups:

# Add a max capacity per clinician
# What if clinicians have specialty constraints?
# What’s the Big O?


import heapq


def balance(caseloads: dict, new_patients: int) -> dict:
    heap = [(count, cid) for cid, count in caseloads.items()]
    heapq.heapify(heap)

    for _ in range(new_patients):
        count, cid = heapq.heappop(heap)
        heapq.heappush(heap, (count + 1, cid))

    return heap


print(balance(caseloads, new_patients))
