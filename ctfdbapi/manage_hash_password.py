import random
import string
from hashlib import sha512


POSSIBILITIES = string.ascii_uppercase + string.digits + string.ascii_lowercase
POSSIBILITIES2 = list(filter(lambda x: False if x in '1lI0oO' else True, POSSIBILITIES))

def generate_str(length=128):
    return ''.join(random.choice(POSSIBILITIES) for x in range(length))
def generate_password(length=128):
    return ''.join(random.choice(POSSIBILITIES2) for x in range(length))

if __name__ == '__main__':
    pw = input("Enter password to hash, empty for random password: ")
    if not pw:
        pw = generate_password(16)
        print("Cleartext Password: " + pw)
    salt = generate_str(128)

    pw_salt = "{}{}".format(pw, salt)
    print("(Hashed) Password (for DB): " + sha512(pw_salt.encode("utf8")).hexdigest())
    print("Password Salt (for DB): " + salt)
