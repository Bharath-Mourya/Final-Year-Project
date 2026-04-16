from sklearn.ensemble import RandomForestClassifier

# ---------------- IMPROVED TRAINING DATA ----------------
# Features: [email_count, keyword_hits, link_count]

X = [
    # LOW RISK
    [0, 0, 1],
    [0, 0, 5],
    [0, 0, 10],

    # MEDIUM RISK (links matter now)
    [0, 0, 50],
    [0, 0, 100],
    [1, 0, 20],
    [0, 1, 30],
    [2, 1, 40],

    # HIGH RISK
    [3, 2, 50],
    [5, 3, 100],
    [6, 4, 150],
    [4, 2, 200],
    [2, 3, 120]
]

# Labels: 0=Low, 1=Medium, 2=High
y = [
    0, 0, 0,
    1, 1, 1, 1, 1,
    2, 2, 2, 2, 2
]

# ---------------- TRAIN MODEL ----------------
model = RandomForestClassifier(n_estimators=50, random_state=42)
model.fit(X, y)


# ---------------- PREDICTION ----------------
import math

def calculate_risk(features):
    email_count = features.get("email_count", 0)
    keyword_hits = features.get("keyword_hits", 0)
    link_count = features.get("link_count", 0)

    prediction = model.predict([[email_count, keyword_hits, link_count]])[0]

    # Feature scaling
    email_factor = email_count * 1.5
    keyword_factor = keyword_hits * 2
    link_factor = math.log(link_count + 1, 10) * 3

    raw_score = email_factor + keyword_factor + link_factor

    if prediction == 0:  # Low
        score = round(min(raw_score, 3), 1)
        level = "Low"

    elif prediction == 1:  # Medium
        normalized = min(raw_score / 6, 1) * 3
        score = round(4 + normalized, 1)
        level = "Medium"

    else:  # High
        normalized = min(raw_score / 6, 1) * 3
        score = round(7 + normalized, 1)
        level = "High"

    return score, level