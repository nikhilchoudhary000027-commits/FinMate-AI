from datetime import date

from modules.savings_planner import calculate_goal_progress

today = date(2026, 10, 20)

# Rs. 60,000 target, Rs. 12,000 saved, target 2027-03-20 (5 months away)
print(calculate_goal_progress(6000000, 1200000, date(2027, 3, 20), today))

# Already achieved
print(calculate_goal_progress(1000000, 1000000, date(2027, 3, 20), today)["status"])

# Overdue
print(calculate_goal_progress(1000000, 200000, date(2026, 9, 1), today)["status"])

# Same month target
print(calculate_goal_progress(1000000, 0, date(2026, 10, 30), today))