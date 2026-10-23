# Text (string)
description = "Lunch at cafe"

# Whole number (integer)
amount_paise = 18000   # Rs. 180.00 stored as paise

# Decimal number (float)
interest_rate = 6.5

# True / False (boolean)
is_expense = True

# Print values and their types
print(description, type(description))
print(amount_paise, type(amount_paise))
print(interest_rate, type(interest_rate))
print(is_expense, type(is_expense))
print(0.1 + 0.2)
print(10 + 20)

amount_rupees = 180.50
amount_paise = round(amount_rupees * 100)
print(amount_paise)
print(amount_paise / 100)