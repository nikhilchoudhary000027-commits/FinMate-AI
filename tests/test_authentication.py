from modules.authentication import register_user, login_user

print(register_user("Asha Rao", "asha@example.com", "asha_01", "Secret123"))
print(register_user("Asha Rao", "asha@example.com", "asha_01", "Secret123"))
print(register_user("Bad", "not-an-email", "bad", "short"))
print(login_user("asha_01", "Secret123"))
print(login_user("asha_01", "WrongPass1"))
print(login_user("nobody", "Secret123"))