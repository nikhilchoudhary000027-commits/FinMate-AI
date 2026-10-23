"""Flag potentially unusual expenses using a robust (median/MAD) z-score."""

import statistics
from collections import defaultdict

MIN_SAMPLES = 5
THRESHOLD = 3.5


def find_unusual(transactions):
    """Return expense transactions that look unusual for their category.

    Each result has the transaction plus 'score' and 'typical_paise'.
    These are potential anomalies only, not proof of fraud or error.
    """
    by_cat = defaultdict(list)
    for t in transactions:
        if t["txn_type"] == "expense":
            by_cat[t["category"]].append(t)

    flagged = []
    for category, items in by_cat.items():
        if len(items) < MIN_SAMPLES:
            continue
        amounts = [t["amount_paise"] for t in items]
        median = statistics.median(amounts)
        mad = statistics.median([abs(a - median) for a in amounts])
        if mad == 0:
            continue  # all amounts almost identical; score undefined
        for t in items:
            score = 0.6745 * (t["amount_paise"] - median) / mad
            if score > THRESHOLD:
                flagged.append({**t, "score": round(score, 1),
                                "typical_paise": round(median)})
    return sorted(flagged, key=lambda t: t["score"], reverse=True)