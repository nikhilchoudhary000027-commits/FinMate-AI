import bcrypt

password = "MySecret123"

hashed = bcrypt.hashpw(password.encode("utf-8"), bcrypt.gensalt())
print("Hash 1:", hashed)

hashed_again = bcrypt.hashpw(password.encode("utf-8"), bcrypt.gensalt())
print("Hash 2:", hashed_again)
print("Hashes same?", hashed == hashed_again)

print("Correct password:", bcrypt.checkpw(password.encode("utf-8"), hashed))
print("Wrong password:  ", bcrypt.checkpw("WrongPass".encode("utf-8"), hashed))