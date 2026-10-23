from modules.simulator import simulate

baseline = {
    "income": 5000000,   # Rs. 50,000
    "expense": 3000000,  # Rs. 30,000
    "savings": 2000000,  # Rs. 20,000
    "by_category": {"Food": 1000000, "Shopping": 800000, "Rent": 1200000},
}

# 1. Food -15%
print(simulate(baseline, reduce_category="Food", reduce_percent=15))
# 2. Save Rs. 2,000 more per month
print(simulate(baseline, extra_saving_paise=200000)["scenario_savings"])
# 3. Income -10%
print(simulate(baseline, income_change_percent=-10)["scenario_savings"])
# 4. No change
print(simulate(baseline)["scenario_total"])