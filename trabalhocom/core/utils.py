import hashlib
import string
import random

def random_key(size=5):
    chars = string.ascii_uppercase + string.digits
    return ''.join(random.choice(chars) for x in range(size))

def generate_hash_key(salt, ramdon_str_size=5):
    ramdon_str = random_key(ramdon_str_size)
    text = ramdon_str + salt
    return hashlib.sha224(text.encode('utf-8')).hexdigest()