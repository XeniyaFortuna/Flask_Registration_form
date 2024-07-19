from werkzeug.security import generate_password_hash, check_password_hash


hash_1 = generate_password_hash('123456')


print(hash_1)
print(check_password_hash(hash_1, '123456'))