# All amounts are in paise (integers)
monthly_budget_paise = 2000000      # Rs. 20,000
spent_paise = 1700000               # Rs. 17,000

percent_used = spent_paise / monthly_budget_paise * 100
print("Budget used:", percent_used, "%")

if percent_used >= 100:
    print("ALERT: Budget exceeded!")
elif percent_used >= 80:
    print("WARNING: You have used 80% or more of your budget.")
else:
    print("You are within your budget.")
expenses_paise = [18000, 25000, 120000, 199900]

total_paise = 0
for amount in expenses_paise:
    total_paise = total_paise + amount
    print("Added", amount, "-> running total:", total_paise)

print("Total spent: Rs.", total_paise / 100)