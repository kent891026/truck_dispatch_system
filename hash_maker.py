
import bcrypt

# boss_password = "1234"
# admin_password = "admin888"
my_password = "admin888"

hashed = bcrypt.hashpw(my_password.encode('utf-8'), bcrypt.gensalt())
print(f"Hashed password: {hashed.decode('utf-8')}")