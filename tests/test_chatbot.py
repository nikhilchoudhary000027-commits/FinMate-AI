from modules.authentication import login_user
from modules.chatbot import handle_message

user = login_user("budget_user", "Secret123")
uid = user["id"]

questions = [
    "How much did I spend this month?",
    "What is my biggest expense category?",
    "How much did I spend on food this month?",
    "Am I over my monthly budget?",
    "How much did I save this month?",
    "How much can I save if I reduce shopping by 20 percent?",
    "Tell me a joke",
]
for q in questions:
    reply, _ = handle_message(uid, q)
    print("Q:", q)
    print("A:", reply)
    print()

reply, pending = handle_message(uid, "I spent 180 rupees on lunch today. Add it.")
print("A:", reply)
print("Pending:", pending)
reply, pending = handle_message(uid, "no", pending)
print("A:", reply, "| Pending:", pending)