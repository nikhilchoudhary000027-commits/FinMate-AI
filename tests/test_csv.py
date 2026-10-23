from modules.authentication import login_user
from modules.csv_tools import export_csv, import_csv

ravi = login_user("ravi_01", "Secret123")

sample = (
    "date,amount,type,description,category\n"
    "2026-10-10,150.50,expense,Test chai,Food\n"
    "2026-10-11,abc,expense,Bad amount,Food\n"
    "2026-10-12,200,expense,Bad category,Nonsense\n"
    "2026-10-13,500,income,Test freelance,Freelance Income\n"
)
print("First import :", import_csv(ravi["id"], sample))
print("Second import:", import_csv(ravi["id"], sample))
print("Bad columns  :", import_csv(ravi["id"], "a,b\n1,2\n"))
print(export_csv(ravi["id"]))