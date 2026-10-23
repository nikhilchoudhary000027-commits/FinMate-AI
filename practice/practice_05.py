# Write a small CSV file
with open("practice/sample.csv", "w", encoding="utf-8") as f:
    f.write("date,amount,description\n")
    f.write("2026-10-20,180,Lunch\n")
    f.write("2026-10-19,250,Uber ride\n")

# Read it back
with open("practice/sample.csv", "r", encoding="utf-8") as f:
    for line in f:
        print(line.strip())
        from datetime import date, datetime

d = datetime.strptime("2026-10-20", "%Y-%m-%d").date()
print(d, d.year, d.month)
print(d.strftime("%B %Y"))
print("Days from today:", (d - date.today()).days)