# Problem 8: Patient Risk Scoring
# Prompt: Build a simple risk scoring system. Given a patient record (dict),
# compute a risk score based on weighted factors.

weights = {
    "missed_appointments": 10,  # points per missed appt
    "declining_scores": 25,  # flat points if True
    "no_emergency_contact": 15,  # flat points if True
    "days_since_last_session": 0.5,  # points per day
}

patient = {
    "name": "Jane Doe",
    "missed_appointments": 3,
    "declining_scores": True,
    "no_emergency_contact": False,
    "days_since_last_session": 45,
}

# risk_score(patient, weights)
# # → 10*3 + 25*1 + 15*0 + 0.5*45 = 30 + 25 + 0 + 22.5 = 77.5

# Expected signature:

# def risk_score(patient: dict, weights: dict) -> float:

# Follow-ups:

# Normalize the score to 0-100 range
# Rank a list of patients by risk
# How would you transition this from rules to ML?


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


print(risk_score(patient, weights))
