from modules.categorization import predict_category

samples = [
    "Spent 180 rupees on lunch",
    "Uber ride 250",
    "Monthly electricity bill 1200",
    "Bought headphones for 1999",
    "Received salary 30000",
    "xyzzy qwerty",
    "",
]
for text in samples:
    print(repr(text), "->", predict_category(text))