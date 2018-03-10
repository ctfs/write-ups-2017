import itertools
import hashlib
import string
import base64
PASSWORD = 'Y2FlZDZhMzZlODNlY2M5Mzk5NDUzZGQ3ZmY0MTQ0OTcyZGI2YTgwZGZkYTBiMzU4MDdkMzUyYTNmN2JhMzc5ZDMxMmRjNDU4MDZiMjZmMzA1NzA1MzdlMjA1ZDAzNDc4MmE1M2FmOTNiMTk1ZWU2ODcwOTJhN2JiNTIzMzYwODE='
SALT = '7049548a11ca1d08d017d2429bb04a3b'
hashed_pw = base64.b64decode(PASSWORD)

# Algorithm:
# base64encode( SHA512 * 512( SHA256 * 256( SHA1 ( MD5 * 5( plaintext + salt ) ) ) ) )
# (SHA512 * 512 means applying SHA512 512 times and all hexdigests are in lowercase)

def repeat_hash(input_t, hash_mode, times):
    for i in range(times):
        input_t = hash_mode(input_t).hexdigest()
    return input_t

def hash_password(password):
    # First step: calculate SHA1 ( MD5 * 5( plaintext + salt ) )
    first = hashlib.sha1(repeat_hash(password + SALT, hashlib.md5, 5)).hexdigest()
    # Second step: SHA256 * 256( first )
    second = repeat_hash(first, hashlib.sha256, 256)
    # Last step: SHA512 * 512( second )
    return repeat_hash(second, hashlib.sha512, 512)

if __name__ == "__main__":
    for i in range(1,5):
        # Create a generator that yields lists of lowercase letters
        generator = itertools.permutations(string.ascii_lowercase, i)
        for test in generator:
            candidate = ''.join(test)
            if hashed_pw == hash_password(candidate):
                print(candidate)
                exit()