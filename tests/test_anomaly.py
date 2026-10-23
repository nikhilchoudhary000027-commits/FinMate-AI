from modules.anomaly_detection import find_unusual

def food(amount, day):
    return {"id": day, "txn_date": f"2026-10-{day:02d}", "amount_paise": amount,
            "txn_type": "expense", "description": "Food", "category": "Food"}

normal = [food(a, i + 1) for i, a in enumerate([15000, 18000, 16000, 17000, 19000, 16500])]
print("Ordinary:", find_unusual(normal))

with_spike = normal + [food(250000, 20)]
result = find_unusual(with_spike)
print("With Rs. 2500 spike:", [(r["amount_paise"], r["score"]) for r in result])

print("Too few:", find_unusual(normal[:3]))
print("Identical:", find_unusual([food(10000, d) for d in range(1, 8)]))