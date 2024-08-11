from werkzeug.security import generate_password_hash, check_password_hash
x = generate_password_hash('admin')
print(generate_password_hash('admin'))

y = check_password_hash(x, "admin")
print(y)