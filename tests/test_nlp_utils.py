from datetime import date

from modules.nlp_utils import (extract_amount_paise, extract_category, extract_date,
                               extract_month, extract_percent)

today = date(2026, 10, 22)
print(extract_amount_paise("I spent 180 rupees on lunch today"))
print(extract_amount_paise("Bought headphones for 1,999"))
print(extract_amount_paise("reduce shopping by 20 percent"))
print(extract_percent("reduce shopping by 20 percent"))
print(extract_category("How much on food last month"))
print(extract_category("hello there"))
print(extract_month("food last month", today), extract_month("this month", today))
print(extract_date("spent 2000 yesterday", today))